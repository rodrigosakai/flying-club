"""
Tests for route [GET] /users/<id>/flights
"""
from random import randint
from mongomock import ObjectId
from src import database
from src.http import HTTP_NOT_FOUND, HTTP_OK
from tests.conftest import MOCK_USER_ID
from tests.integration import utils


def test_not_found_student(client):
    """
    Tests whether endpoint returns HTTP_NOT_FOUND if given id doesn't belong to a student
    """
    response = client.get(f"/users/{MOCK_USER_ID}/flights")

    assert response.status_code == HTTP_NOT_FOUND


def test_success(client):
    """
    Tests whether endpoint returns HTTP_OK and flights if id is a valid student id
    """
    database.insert_document(
        {"_id": ObjectId(MOCK_USER_ID),
         "role": "student"},
        "users")

    student_flights_count = randint(2, 10)

    for _ in range(student_flights_count):
        database.insert_document(
            {"student_id": MOCK_USER_ID},
            "flights")

    response = client.get(f"/users/{MOCK_USER_ID}/flights")

    response_data = utils.convert_response_data_to_dict(response.data)

    assert response.status_code == HTTP_OK \
        and len(response_data) == student_flights_count
