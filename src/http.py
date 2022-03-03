"""
HTTP module
"""
import logging
from functools import wraps
from types import FunctionType
from enum import Enum
import jsonschema
from flask import request, abort

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# 200
HTTP_OK = 200
HTTP_CREATED = 201

# 400
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_PAYLOAD_TOO_LARGE = 413
HTTP_UNSUPORTED_MEDIA_TYPE = 415

MAX_CONTENT_LENGTH = 10**4


class MediaType(Enum):
    """
    Request media types
    """
    APPLICATION_JSON = "application/json"


def validate_request(media_type: MediaType, max_content_length: int = MAX_CONTENT_LENGTH,
                     schema: dict = None):
    """
    Validates incoming request, by checking wheter:
        1. Request media type matches the one specified in the endpoint;
        2. Request content length
        3. Payload schema, if provided one

    Params:
    --------
    media_type: str
        Enum specified in MediaType class
    max_content_length: int
        Maximum content length specified in endpoint. By default, it is constant MAX_CONTENT_LENGTH
    schema: dict
        JSON schema for specified route
    """
    def decorator(func: FunctionType):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.content_length > max_content_length:
                logger.warning(
                    """Request with payload too large: %s kB.
                    Maximum accepted for endpoint %s %s is: %s""",
                    request.content_length, request.method, request.path, max_content_length)
                abort(HTTP_PAYLOAD_TOO_LARGE)

            if request.content_type != media_type.value:
                logger.warning(
                    "Request with unsuported media type: %s. %s %s accepts %s",
                    request.content_type, request.method, request.path, media_type.value)
                abort(HTTP_UNSUPORTED_MEDIA_TYPE)

            if not schema:
                return func(*args, **kwargs)

            try:
                jsonschema.validate(request.json, schema)
            except jsonschema.ValidationError as validation_error:
                logger.warning(
                    """Error validating JSON schema for route %s %s.
                    Error: %s. Path in schema: %s""",
                    request.method, request.path, validation_error.message,
                    list(validation_error.schema_path))
                return {
                    "message": "request didn't follow expected schema",
                    "error": validation_error.message}, HTTP_BAD_REQUEST

            return func(*args, **kwargs)
        return wrapper
    return decorator
