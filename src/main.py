from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from playhouse.shortcuts import model_to_dict

from models.event import Event, User, db
from models.new_event_request import NewEventRequest
from src import ValidationException
from models.get_events_by_day_request import GetEventsByDayRequest
from models.mark_as_done_request import MarkAsDoneRequest

with db:
    db.create_tables([Event, User])

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/event", methods=["GET"])
@cross_origin(supports_credentials=True)
# Returns all of events
def get_events():
    all_events = [event for event in Event.select().dicts()]
    return jsonify(all_events)


@app.route("/event/new", methods=['POST'])
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
    Event(title=body.title, date=f"{body.date} {body.time}", user_id=body.user_id, is_done=False).save()

    return get_events()


@app.route("/event/check-as-done", methods=['POST'])
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


@app.route("/event/get-all-by-date", methods=['POST'])
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


if __name__ == "__main__":
    app.run(port=8080, debug=True)
