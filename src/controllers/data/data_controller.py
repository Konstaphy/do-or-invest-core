from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import csv

from src.exceptions.validation_exception import ValidationException
from src.models.requests.set_new_data import NewDataRequest

dataController = Blueprint("data", __name__, url_prefix="/data")


@dataController.route("/", methods=["POST"])
@cross_origin(supports_credentials=True)
def set_new_data():
    try:
        data = NewDataRequest(request.get_json(force=True))
    except ValidationException:
        return "ValidationError", 400

    with open("train.csv", 'a') as table:
        fieldnames = ["data", "result"]
        writer = csv.DictWriter(table, fieldnames=fieldnames, delimiter=",")
        writer.writerow({"data": data.description, "result": data.priority})
    with open("train.csv", 'r') as table:
        return jsonify({"sum": sum(1 for _ in table)})
