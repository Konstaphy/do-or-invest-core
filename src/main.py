from flask import Flask, jsonify, request
from flask_cors import CORS
from db.init import init_database
import uuid

import sqlite3
app = Flask(__name__)
cors = CORS(app)

with sqlite3.connect("db/database.db", check_same_thread=False) as db:
    init_database(db.cursor())

@app.route("/")
def hello_world():
    with sqlite3.connect("db/database.db", check_same_thread=False) as db:
        cursor = db.cursor()
        query = """select * from Events"""
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return jsonify({'events': records})

@app.route("/event/new", methods=['POST'])
def post_event():
    input_json = request.get_json(force=True)
    print(input_json["hello"])
    with sqlite3.connect("db/database.db", check_same_thread=False) as db:
        cursor = db.cursor()
        query = """
            insert into Events (id, title, startDate, endDate, userId, done) values (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (str(uuid.uuid4()), "123", "10-10-2022", "20-10-2022", str(uuid.uuid4()), False))
        cursor.close()

    return "ready"

app.run(debug=True)