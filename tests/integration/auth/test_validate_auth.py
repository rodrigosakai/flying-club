"""
Test if routes are protected by @auth.validate_auth
"""
import json
from src.http import HTTP_UNAUTHORIZED

from tests.integration.utils import generate_invalid_headers

with open("tests/integration/auth/validate_auth.json", "r", encoding="utf-8") as f:
    ROUTES = json.load(f)


def test_get_routes(client):
    """
    Tests if GET routes are protected against unauthorized roles
    """
    get_routes = ROUTES["get"]
    unauthorized_count = 0
    expected_unauthorized_count = 0

    for route in get_routes:
        endpoint = route["endpoint"]
        unauthorized_roles = route["unauthorized_roles"]

        expected_unauthorized_count += len(unauthorized_roles)

        for role in unauthorized_roles:
            headers = generate_invalid_headers(role)
            response = client.get(
                endpoint,
                headers=headers
            )

            if response.status_code == HTTP_UNAUTHORIZED:
                unauthorized_count += 1

    assert unauthorized_count == expected_unauthorized_count
