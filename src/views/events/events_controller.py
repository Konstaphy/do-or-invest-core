from datetime import datetime

import jwt
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.exceptions.validation_exception import ValidationException
from src.models.event import Event
from src.models.requests.get_events_by_day_request import GetEventsByDayRequest
from src.models.requests.mark_as_done_request import MarkAsDoneRequest
from src.models.requests.new_event_request import NewEventRequest
from src.models.user import User
from src.utils.compare_dates import is_date_less, is_date_more, is_date_equal

events = Blueprint("events", __name__, url_prefix="/events")


@events.route("/")
@cross_origin(supports_credentials=True)
def get_events():
    all_events = [event for event in Event.select().dicts()]
    return jsonify(all_events)


@events.route("/new", methods=['POST'])
@cross_origin(supports_credentials=True)
# Creates a new Event
def post_event():
    try:
        # Parsing request
        input_json = request.get_json(force=True)
        body = NewEventRequest(input_json)
    except ValidationException:
        # If data is not valid throw an Error
        return jsonify({"message": "Bad request - 400"}), 400

    # Creating new event
    Event(title=body.title, date=f"{body.date} {body.time}", user_id=body.user_id, priority=0, is_done=False,
          is_expired=False).save()

    return get_events()


@events.route("/check-as-done", methods=['POST'])
@cross_origin(supports_credentials=True)
def check_as_done():
    try:
        # Parsing request
        input_json = request.get_json(force=True)
        body = MarkAsDoneRequest(input_json)
    except ValidationException:
        # If data is not valid throw an Error
        return jsonify({"message": "Bad request - 400"}), 400
    query = Event.update(is_done=True).where(id=body.event_id)
    query.execute()
    return get_events()


@events.route("/check-expired")
@cross_origin(supports_credentials=True)
def check_expired():
    token = request.headers.get("authorization").split(" ")[1]
    if token is None:
        return "Unauthorized", 401

    try:
        data = jwt.decode(token, "secret", algorithms="HS256")
    except jwt.exceptions.ExpiredSignatureError:
        return "Unauthorized", 401

    if data.get("id") is None:
        return "Unauthorized", 401

    user_events = Event.select().where(Event.user_id == data.get("id"))
    user = User.get(User.id == data.get("id"))
    penalty = 0
    for event in user_events:
        if is_date_less(event.date, datetime.now()) and not event.is_expired:
            query = Event.update(is_expired=True).where(Event.id == event.id)
            query.execute()
            penalty += event.priority

    user_query = User.update(penalty=user.penalty + penalty).where(User.id == data.get("id"))
    user_query.execute()
    return get_events()


@events.route("/get-all-by-date", methods=['POST'])
@cross_origin(supports_credentials=True)
def get_all_by_date():
    try:
        # Parsing request
        input_json = request.get_json(force=True)
        body = GetEventsByDayRequest(input_json)
    except ValidationException:
        # If data is not valid throw an Error
        return jsonify({"message": "Bad request - 400"}), 400
    # Selecting all events dated as the date in body
    res = Event.select() \
        .where((Event.date.year == datetime.fromisoformat(body.date).year) & (
            Event.date.month == datetime.fromisoformat(body.date).month) & (
                       Event.date.day == datetime.fromisoformat(body.date).day
               )) \
        .dicts()
    return jsonify([e for e in res])
