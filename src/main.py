from flask import Flask
from flask_cors import CORS
from src.models.event import Event
from src.models.entity import db
from src.models.user import User
from src.views.events.events_controller import events

if __name__ == "__main__":
    with db: db.create_tables([Event, User])

    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(events)
    app.run(port=8080, debug=True)
