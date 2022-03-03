"""
Common functions to integrating testing
"""
import json
from src import auth


def convert_response_data_to_dict(response_data: bytes) -> dict:
    """
    Converts flask test client response object to dict

    Params:
    -------
    response_data: bytes
        Flask test client response data

    Returns:
    -------
    dict: Response data object as dict
    """
    return json.loads(response_data.decode("utf-8"))


def generate_invalid_headers(unauthorized_role: str) -> dict:
    """
    Generates headers with specified role

    Params:
    -------
    unauthorized_role: str

    Returns:
    -------
    dict: invalid header
    """
    if unauthorized_role is None:
        return {}

    with open("tests/mock/user.json", "r", encoding="utf-8") as mock_user_json:
        mock_user = json.load(mock_user_json)
        mock_user["role"] = unauthorized_role

        token = auth.generate_jwt_token(mock_user)
        return {"Authorization": f"Bearer {token}"}
