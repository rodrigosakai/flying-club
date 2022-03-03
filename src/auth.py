"""
Authentication module
"""
from functools import wraps
import logging
import os
from enum import Enum
from types import FunctionType
import bcrypt
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from flask import request, abort
from src import date
from src.http import HTTP_UNAUTHORIZED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise RuntimeError("No secret key found in environment")


class UserRole(Enum):
    """
    User roles
    """
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    PILOT = "pilot"


class JWTAuthenticator:
    """
    Authenticates bearer
    """

    def __init__(self):
        request_authorization = request.headers.get("Authorization")
        if request_authorization is None:
            self.token = ""

        request_authorization_list = request_authorization.split()
        if len(request_authorization_list) != 2:
            self.token = ""

        self.token = request_authorization_list[1]

    def __decode_token_from_headers(self):
        """
        Decodes token
        """
        return jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])

    def is_token_valid(self):
        """
        Validates whether token in request headers is valid

        Returns:
        --------
        bool: validation result
        dict: payload, if token is valid. Otherwise, empty dict
        """
        try:
            self.__decode_token_from_headers()

            return True
        except (ExpiredSignatureError, InvalidSignatureError):
            return False

    def get_user_role(self) -> str:
        """
        Retrieves user role from headers token

        Returns:
        -------
        str: user role
        """
        payload = self.__decode_token_from_headers()
        return payload.get("role")


def generate_jwt_token(user: dict) -> str:
    """
    Generates JWT token with app secret key

    Params:
    -------
    user: dict
        User document from database

    Returns:
    -------
    str: JWT token
    """
    payload = {
        key: user[key] for key in user if key not in ("_id", "password")
    }

    payload["exp"] = date.get_24_hours_from_now()

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validate_auth(authorized_enums: list):
    """
    Validates if incoming JWT token is valid
    """
    def decorator(func: FunctionType):
        @wraps(func)
        def wrapper(*args, **kwargs):
            jwt_authenticator = JWTAuthenticator()
            if not jwt_authenticator.is_token_valid():
                abort(HTTP_UNAUTHORIZED)

            authorized_roles = {
                enum_role.value for enum_role in authorized_enums}

            if jwt_authenticator.get_user_role() not in authorized_roles:
                abort(HTTP_UNAUTHORIZED)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def is_password_valid(password: str, hashed_password: bytes) -> bool:
    """
    Checks whether user informed password matches the one stored in database

    Params:
    -------
    password: str
        User informed password
    hashed_password: bytes
        Hashed password in database

    Returns:
    -------
    bool: result of verification
    """
    bytes_password = bytes(password, encoding="utf-8")
    return bcrypt.checkpw(bytes_password, hashed_password)
