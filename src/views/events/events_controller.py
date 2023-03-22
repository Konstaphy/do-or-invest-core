from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.exceptions.validation_exception import ValidationException
from src.models.event import Event
from src.models.requests.get_events_by_day_request import GetEventsByDayRequest
from src.models.requests.mark_as_done_request import MarkAsDoneRequest
from src.models.requests.new_event_request import NewEventRequest

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
    Event(title=body.title, date=f"{body.date} {body.time}", user_id=body.user_id, priority=0, is_done=False).save()

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
