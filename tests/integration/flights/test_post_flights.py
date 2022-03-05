"""
Tests for route [POST] /flights
"""
import json
import os
from src import database
from src.http import HTTP_BAD_REQUEST, HTTP_CREATED
from tests.conftest import APPLICATION_JSON, MOCK_USER_ID
from tests.integration import utils

MINIMUM_FLYING_HOURS = int(os.getenv("MINIMUM_FLYING_HOURS"))


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


def test_cant_issue_licence(client, instructor_headers, mock_flight):
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

    response_data = utils.convert_response_data_to_dict(response.data)

    assert response.status_code == HTTP_CREATED \
        and not response_data["can_issue_licence"] \
        and len(flights) == 1


def test_can_issue_licence(client, instructor_headers, mock_flight):
    """
    Tests whether endpoint:
        1. creates flying record
        2. 'can_issue_licence' is True
        3. returns HTTP_CREATED
    """
    database.insert_document(
        {"student_id": MOCK_USER_ID,
         "duration": MINIMUM_FLYING_HOURS-1,
         "grade": 4},
        "flights")

    response = client.post(
        "/flights",
        content_type=APPLICATION_JSON,
        data=json.dumps(mock_flight),
        headers=instructor_headers
    )

    flights = database.get_documents("flights", {"student_id": MOCK_USER_ID})

    response_data = utils.convert_response_data_to_dict(response.data)

    assert response.status_code == HTTP_CREATED \
        and response_data["can_issue_licence"] \
        and len(flights) == 2
