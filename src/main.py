from flask import Flask
from flask_cors import CORS

from src.controllers.data.data_controller import dataController
from src.models.event import Event
from src.models.entity import db
from src.models.user import User
from src.controllers.events.events_controller import events
from src.controllers.users.users_controller import users

with db:
    db.create_tables([Event, User])

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(events)
    app.register_blueprint(dataController)
    app.register_blueprint(users)
    app.run(port=8080, debug=True)
