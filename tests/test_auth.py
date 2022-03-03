"""
Tests for auth module
"""
import os
import jwt
from src import auth
from tests.conftest import MOCK_PASSWORD, MOCK_HASHED_PASSWORD
SECRET_KEY = os.getenv("SECRET_KEY")


def test_generate_jwt_token(mock_user):
    """
    Tests if decoded JWT token has user info
    """
    mock_user["role"] = "instructor"

    token = auth.generate_jwt_token(mock_user)

    user_dict = jwt.decode(token, SECRET_KEY, ["HS256"])

    assert user_dict["email"] == mock_user["email"] \
        and user_dict["role"] == mock_user["role"]


def test_success_is_password_valid():
    """
    Tests if function returns True when correct password is submitted
    """
    assert auth.is_password_valid(MOCK_PASSWORD, MOCK_HASHED_PASSWORD)


def test_fail_is_password_valid():
    """
    Tests if function returns False when wrong password is submitted
    """
    assert not auth.is_password_valid("abc", MOCK_HASHED_PASSWORD)
