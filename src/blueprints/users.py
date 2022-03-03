"""
users Blueprint
"""
import json
from flask import Blueprint, request
from bson import json_util
from src import database, http
from src.http import HTTP_CREATED, MediaType

users_bp = Blueprint("users_bp", __name__)

with open("src/json/users/instructor.json", "r", encoding="utf-8") as f:
    POST_SCHEMA = json.load(f)


@users_bp.route("/", methods=["GET"])
def get_users():
    """
    Returns documents from users collection
    """
    return json_util.dumps(database.get_documents("users"))


@users_bp.route("/", methods=["POST"])
@http.validate_request(MediaType.APPLICATION_JSON, schema=POST_SCHEMA)
def create_user():
    """
    Create user in users collection. A user is either:
        - A student
        - A pilot
        - An instructor
    """
    user_id, timestamp = database.insert_document(request.json, "users")

    return {"user_id": user_id, "created_at": timestamp}, HTTP_CREATED


@users_bp.route("/<string:user_id>", methods=["PUT"])
@http.validate_request(MediaType.APPLICATION_JSON, schema=POST_SCHEMA)
def update_user(user_id):
    """
    Updates user information in database
    """
    timestamp = database.update_document(user_id, "users", request.json)

    return {"updated_at": timestamp}
