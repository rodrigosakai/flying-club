"""
Tests setup
"""
import os
from unittest import mock
import json
import bcrypt
import pytest
import mongomock
from bson.objectid import ObjectId
from api import app
from src import auth, database
from src.http import MediaType

MINIMUM_FLYING_HOURS = int(os.getenv("MINIMUM_FLYING_HOURS"))
APPLICATION_JSON = MediaType.APPLICATION_JSON.value
MOCK_EMAIL = "mock@test.com"
MOCK_USER_ID = str(ObjectId())
MOCK_PASSWORD = "mock-password"
MOCK_HASHED_PASSWORD = bcrypt.hashpw(
    bytes(MOCK_PASSWORD, "utf-8"),
    bcrypt.gensalt())


@pytest.fixture
def client():
    """
    Injects client into tests
    """
    with app.test_client() as app_test_client:
        yield app_test_client


@pytest.fixture(autouse=True)
def patch_mongo_client():
    """
    Injects clean mock database to each test
    """
    mock_db = mongomock.Database(mongomock.MongoClient(), "", _store=None)
    with mock.patch.object(database, "db", mock_db):
        yield


@pytest.fixture
def mock_user():
    """
    Injects mock user into tests
    """
    with open("tests/mock/user.json", "r", encoding="utf-8") as mock_user_file:
        user_json = json.load(mock_user_file)
        user_json["email"] = MOCK_EMAIL
        user_json["password"] = MOCK_HASHED_PASSWORD
        yield user_json


@pytest.fixture
def instructor_headers():
    """
    Injects headers with instructor role to access protected routes
    """
    with open("tests/mock/user.json", "r", encoding="utf-8") as mock_user_file:
        user = json.load(mock_user_file)
        user["role"] = "instructor"
        token = auth.generate_jwt_token(user)

        yield {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_pilot():
    """
    Injects mock pilot into tests
    """
    with open("tests/mock/pilot.json", "r", encoding="utf-8") as mock_pilot_file:
        yield json.load(mock_pilot_file)


@pytest.fixture
def mock_instructor():
    """
    Injects mock instructor into tests
    """
    with open("tests/mock/instructor.json", "r", encoding="utf-8") as mock_instructor_file:
        yield json.load(mock_instructor_file)


@pytest.fixture
def mock_student():
    """
    Injects mock instructor into tests
    """
    with open("tests/mock/student.json", "r", encoding="utf-8") as mock_student_file:
        yield json.load(mock_student_file)


@pytest.fixture
def mock_flight():
    """
    Injects mock flight into tests
    """
    with open("tests/mock/flight.json", "r", encoding="utf-8") as mock_flight_file:
        mock_flight_json = json.load(mock_flight_file)
        mock_flight_json["student_id"] = MOCK_USER_ID
        yield mock_flight_json
