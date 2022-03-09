"""
Tests for route [POST] /users/<id>/licence
"""
from bson.objectid import ObjectId
from src import database
from src.auth import UserRole
from src.http import HTTP_BAD_REQUEST, HTTP_OK
from tests.conftest import MOCK_USER_ID, MINIMUM_FLYING_HOURS


def test_can_issue_licence(client, instructor_headers):
    """
    Tests whether:
        1. Route converts student into pilot, when student has enough high grade flying hours;
        2. Route returns HTTP_OK
    """
    database.insert_document(
        {"_id": ObjectId(MOCK_USER_ID),
         "role": UserRole.STUDENT.value},
        "users")

    database.insert_document(
        {"student_id": MOCK_USER_ID,
         "duration": MINIMUM_FLYING_HOURS,
         "grade": 4},
        "flights")

    response = client.post(
        f"/users/{MOCK_USER_ID}/licence",
        headers=instructor_headers)

    user = database.get_documents("users", {"_id": ObjectId(MOCK_USER_ID)})[0]

    assert user["role"] == UserRole.PILOT.value\
        and "licence_number" in user \
        and response.status_code == HTTP_OK


def test_cannot_issue_licence(client, instructor_headers):
    """
    Tests whether route returns HTTP_BAD_REQUEST when student doesn't have enough high grade flying hours
    """
    database.insert_document(
        {"_id": ObjectId(MOCK_USER_ID),
         "role": UserRole.STUDENT.value},
        "users")

    response = client.post(
        f"/users/{MOCK_USER_ID}/licence",
        headers=instructor_headers)

    user = database.get_documents("users", {"_id": ObjectId(MOCK_USER_ID)})[0]

    assert response.status_code == HTTP_BAD_REQUEST \
        and user["role"] == UserRole.STUDENT.value
