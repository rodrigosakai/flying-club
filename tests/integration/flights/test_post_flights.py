"""
Tests for route [POST] /flights
"""
import json
from src import database
from src.http import HTTP_BAD_REQUEST, HTTP_CREATED
from tests.conftest import APPLICATION_JSON, MOCK_USER_ID


def test_bad_request(client, instructor_headers):
    """
    Tests whether endpoint returns HTTP_BAD_REQUEST if payload is invalid
    """
    response = client.post(
        "/flights",
        content_type=APPLICATION_JSON,
        data=json.dumps({}),
        headers=instructor_headers)

    assert response.status_code == HTTP_BAD_REQUEST


def test_success(client, instructor_headers, mock_flight):
    """
    Tests whether endpoint:
        1. creates flying record
        2. 'can_issue_licence' is False
        3. returns HTTP_CREATED
    """
    response = client.post(
        "/flights",
        content_type=APPLICATION_JSON,
        data=json.dumps(mock_flight),
        headers=instructor_headers
    )

    flights = database.get_documents("flights", {"student_id": MOCK_USER_ID})

    assert response.status_code == HTTP_CREATED \
        and len(flights) == 1
