"""
Integration tests for login route
"""
import json
from src.http import HTTP_BAD_REQUEST, HTTP_NOT_FOUND, HTTP_OK, HTTP_UNAUTHORIZED
from src import database
from tests.conftest import APPLICATION_JSON, MOCK_EMAIL, MOCK_PASSWORD


def test_bad_request(client):
    """
    Tests schema's route by sending invalid payload
    """
    response = client.post(
        "/login",
        data=json.dumps({}),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == HTTP_BAD_REQUEST


def test_not_found(client):
    """
    Tests if route returns HTTP_NOT_FOUND if email doesn't exist in database
    """
    response = client.post(
        "/login",
        data=json.dumps({
            "email": "not-real@mock.com",
            "password": "not-relevant"
        }),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == HTTP_NOT_FOUND


def test_wrong_password(client, mock_user):
    """
    Tests if route returns HTTP_UNAUTHORIZED if wrong password is submitted
    """
    database.insert_document(
        mock_user,
        "users")

    response = client.post(
        "/login",
        data=json.dumps({
            "email": MOCK_EMAIL,
            "password": "wrong-password"
        }),
        content_type=APPLICATION_JSON
    )

    assert response.status_code == HTTP_UNAUTHORIZED


def test_succes(client, mock_user):
    """
    Tests whether route returns HTTP_OK if user provides correct credentials
    """
    database.insert_document(mock_user, "users")

    response = client.post(
        "/login",
        data=json.dumps({
            "email": MOCK_EMAIL,
            "password": MOCK_PASSWORD
        }),
        content_type=APPLICATION_JSON)

    assert response.status_code == HTTP_OK
