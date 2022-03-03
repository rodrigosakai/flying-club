"""
Auth blueprint
"""
import logging
import json
from flask import Blueprint, request, abort
from src import http, auth, database
from src.http import HTTP_NOT_FOUND, HTTP_UNAUTHORIZED, MediaType

logger = logging.getLogger()

auth_bp = Blueprint("auth_bp", __name__)

with open("src/json/auth/login.json", "r", encoding="utf-8") as f:
    LOGIN_SCHEMA = json.load(f)


@auth_bp.route("/login", methods=["POST"])
@http.validate_request(MediaType.APPLICATION_JSON, schema=LOGIN_SCHEMA)
def login():
    """
    Authenticates user
    """
    email = request.json["email"]
    logger.info("User %s requested login", email)

    users = database.get_documents("users", {"email": email})
    if not users:
        logger.warning("User not registered in database")
        abort(HTTP_NOT_FOUND)

    user = users[0]
    password = request.json["password"]
    hashed_password = user["password"]

    if not auth.is_password_valid(password, hashed_password):
        logger.warning("User provided wrong password")
        abort(HTTP_UNAUTHORIZED)

    token = auth.generate_jwt_token(user)

    return {"token": token}
