from flask import Flask, jsonify, request
from flask_cors import CORS
from db.init import init_database
import uuid

import sqlite3

app = Flask(__name__)
cors = CORS(app)

with sqlite3.connect("db/database.db") as db:
    init_database(db.cursor())


@app.route("/event")
def get_events():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        query = """select * from Events"""
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        records = list(map(
            lambda x: {"id": x[0], "title": x[1], "day": x[2], "user_id": x[3], "is_done": bool(x[4])}, records))
        return jsonify({"events": records})


@app.route("/event/new", methods=['POST'])
def post_event():
    input_json = request.get_json(force=True)
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        query = """
            insert into Events (id, title, day, userId, done) values (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (str(uuid.uuid4()),
                               input_json["title"],
                               input_json["day"],
                               input_json["user_id"],
                               input_json["is_done"]))
        cursor.execute("""select * from Events""")
        records = cursor.fetchall()
        records = list(map(
            lambda x: {"id": x[0], "title": x[1], "day": x[2], "user_id": x[3], "is_done": bool(x[4])}, records))
        cursor.close()

        return jsonify({"events": records})


@app.route("/event/check-as-done", methods=['POST'])
def check_as_done():
    input_json = request.get_json(force=True)
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        query = """
            update Events set done = ? where id = ?
        """
        cursor.execute(query, (input_json["is_done"], input_json["event_id"]))
        cursor.close()

    return "ready"


app.run(debug=True)
