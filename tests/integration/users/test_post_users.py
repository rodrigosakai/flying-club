"""
Tests for route [POST] /users
"""
import json
from src.http import HTTP_BAD_REQUEST, HTTP_CREATED
from tests.conftest import APPLICATION_JSON
from src import database


def test_success(client, mock_instructor, mock_pilot, mock_student):
    """
    For each user schema, tests if:
        1. record is inserted into database upon valid payload
        2. endpoint returns HTTP_CREATED
    """
    schemas = [mock_instructor, mock_pilot, mock_student]
    created_count = 0

    for user in schemas:
        response = client.post(
            "/users",
            data=json.dumps(user),
            content_type=APPLICATION_JSON
        )

        if response.status_code == HTTP_CREATED:
            created_count += 1

    users = database.get_documents("users")

    assert len(users) == len(schemas) == created_count


def test_invalid_payload(client):
    """
    Tests whether schema verification returns HTTP_BAD_REQUEST
    """
    response = client.post(
        "/users",
        data=json.dumps({}),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == HTTP_BAD_REQUEST
