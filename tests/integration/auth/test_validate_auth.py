"""
Test if routes are protected by @auth.validate_auth
"""
import json
from src.http import HTTP_UNAUTHORIZED
from tests.conftest import APPLICATION_JSON
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


def test_post_routes(client):
    """
    Tests if POST routes are protected against unauthorized roles
    """
    post_routes = ROUTES["post"]
    unauthorized_count = 0
    expected_unauthorized_count = 0

    for route in post_routes:
        endpoint = route["endpoint"]
        unauthorized_roles = route["unauthorized_roles"]

        expected_unauthorized_count += len(unauthorized_roles)

        for role in unauthorized_roles:
            headers = generate_invalid_headers(role)
            response = client.post(
                endpoint,
                headers=headers,
                data=json.dumps({}),
                content_type=APPLICATION_JSON
            )

            if response.status_code == HTTP_UNAUTHORIZED:
                unauthorized_count += 1

    assert unauthorized_count == expected_unauthorized_count
