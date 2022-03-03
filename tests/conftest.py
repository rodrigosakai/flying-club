"""
Tests setup
"""
import json
import bcrypt
import pytest
from api import app
from src.http import MediaType


APPLICATION_JSON = MediaType.APPLICATION_JSON.value
MOCK_EMAIL = "mock@test.com"

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


@pytest.fixture
def mock_user():
    """
    Injects mock user into tests
    """
    with open("tests/mock/user.json", "r", encoding="utf-8") as mock_user_json:
        user = json.load(mock_user_json)
        user["email"] = MOCK_EMAIL
        user["password"] = MOCK_HASHED_PASSWORD
        yield user
