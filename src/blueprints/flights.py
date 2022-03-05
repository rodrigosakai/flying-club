"""
Flights blueprint
"""
import json
from flask import Blueprint, request
from src import http, auth, database, licence
from src.auth import UserRole
from src.http import HTTP_CREATED, MediaType

flights_bp = Blueprint("flights_bp", __name__)

with open("src/json/flights/post.json", "r", encoding="utf-8") as f:
    POST_SCHEMA = json.load(f)


@flights_bp.route("/", methods=["POST"])
@auth.validate_auth([UserRole.INSTRUCTOR])
@http.validate_request(MediaType.APPLICATION_JSON, schema=POST_SCHEMA)
def register_flight():
    """
    Registers a flying class.
    """
    flight_id, timestamp = database.insert_document(request.json, "flights")
    student_id = request.json["student_id"]

    return {
        "flight_id": flight_id,
        "timestamp": timestamp,
        "can_issue_licence": licence.can_issue(student_id)
    }, HTTP_CREATED
