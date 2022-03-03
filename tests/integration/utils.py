"""
Common functions to integrating testing
"""


import json


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
