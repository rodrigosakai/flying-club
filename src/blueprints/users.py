"""
users Blueprint
"""
import json
from flask import Blueprint, request, abort
from bson import json_util
from src import http, database, auth, flying_license
from src.auth import UserRole
from src.http import HTTP_BAD_REQUEST, HTTP_CREATED, MediaType

users_bp = Blueprint("users_bp", __name__)

with open("src/json/users/instructor.json", "r", encoding="utf-8") as f:
    INSTRUCTOR_SCHEMA = json.load(f)
with open("src/json/users/pilot.json", "r", encoding="utf-8") as f:
    PILOT_SCHEMA = json.load(f)
with open("src/json/users/student.json", "r", encoding="utf-8") as f:
    STUDENT_SCHEMA = json.load(f)

POST_SCHEMA = {"oneOf": [INSTRUCTOR_SCHEMA, PILOT_SCHEMA, STUDENT_SCHEMA]}


@users_bp.route("/", methods=["GET"])
@auth.validate_auth([UserRole.INSTRUCTOR, UserRole.PILOT, UserRole.STUDENT])
def get_users():
    """
    [GET] /users

    Returns documents from users collection
    """
    return json_util.dumps(database.get_documents("users"))


@users_bp.route("/", methods=["POST"])
@http.validate_request(MediaType.APPLICATION_JSON, schema=POST_SCHEMA)
def create_user():
    """
    [POST] /users

    Create user in users collection. A user is either:
        - A student
        - A pilot
        - An instructor
    """
    created_id, timestamp = database.insert_document(request.json, "users")

    return {"user_id": created_id, "created_at": timestamp}, HTTP_CREATED


@users_bp.route("/<string:user_id>/flights", methods=["GET"])
@database.validate_student_id()
def get_user_flights(user_id: str):
    """
    [GET] /users/<id>/flights

    Retrieves student's flights records in database.
    """
    user_flights = database.get_documents(
        "flights",
        {"student_id": user_id})

    return json_util.dumps(user_flights)


@users_bp.route("/<string:user_id>", methods=["PUT"])
@http.validate_request(MediaType.APPLICATION_JSON, schema=POST_SCHEMA)
def update_user(user_id: str):
    """
    [PUT] /users/<id>

    Updates user data in database
    """
    timestamp = database.update_document(user_id, "users", request.json)

    return {"updated_at": timestamp}


@users_bp.route("/<string:user_id>/licence", methods=["POST"])
@auth.validate_auth([UserRole.INSTRUCTOR])
@database.validate_student_id()
def issue_licence(user_id):
    """
    [POST] /users/<id>/licence

    Converts student into pilot, if student has enough high grade flying hours
    """
    if not flying_license.can_issue(user_id):
        abort(HTTP_BAD_REQUEST)

    licence_number = flying_license.issue()

    timestamp = database.update_document(
        user_id,
        "users",
        {"role": UserRole.PILOT.value, "licence_number": licence_number})

    return {"timestamp": timestamp}
