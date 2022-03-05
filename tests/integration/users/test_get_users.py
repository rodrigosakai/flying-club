"""
Tests for route [GET] /users
"""
from random import randint
from src import database
from src.http import HTTP_OK
from tests.conftest import APPLICATION_JSON
from tests.integration import utils


def test_success(client, instructor_headers):
    """
    Tests whether a request with valid authorization returns documents in the user collection
    """
    user_count = randint(2, 5)
    for _ in range(user_count):
        database.insert_document({}, "users")

    response = client.get(
        "/users",
        content_type=APPLICATION_JSON,
        headers=instructor_headers
    )

    response_data = utils.convert_response_data_to_dict(response.data)

    assert len(response_data) == user_count \
        and response.status_code == HTTP_OK
