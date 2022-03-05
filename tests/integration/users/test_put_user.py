"""
Tests for route [PUT] /users/<id>
"""
import json
from bson.objectid import ObjectId
from src import database
from src.http import HTTP_BAD_REQUEST, HTTP_OK
from tests.conftest import APPLICATION_JSON, MOCK_USER_ID


def test_success_update(client, mock_pilot, mock_student, mock_instructor):
    """
    For all user roles, tests if:
        1. User record is updated with incoming valid payload
        2. Route returns HTTP_OK
    """
    success_count = 0
    roles = [mock_pilot, mock_student, mock_instructor]

    for user in roles:
        database.insert_document(
            {"_id": ObjectId(MOCK_USER_ID)},
            "users")

        response = client.put(
            f"/users/{MOCK_USER_ID}",
            data=json.dumps(mock_pilot),
            content_type=APPLICATION_JSON)

        user = database.get_documents(
            "users", {"_id": ObjectId(MOCK_USER_ID)})[0]
        validator = {key: user[key] for key in user}

        if response.status_code == HTTP_OK and validator == user:
            success_count += 1

        database.delete_document(MOCK_USER_ID, "users")

    assert success_count == len(roles)


def test_bad_request(client):
    """
    Tests if route returns HTTP_BAD_REQUEST with invalid payload
    """
    response = client.put(
        "/users/mock-id",
        data=json.dumps({}),
        content_type=APPLICATION_JSON)

    assert response.status_code == HTTP_BAD_REQUEST
