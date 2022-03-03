"""
Date/time module
"""
import datetime
import pytz

SAO_PAULO_TIMEZONE = pytz.timezone("America/Sao_Paulo")


def get_current_timestamp() -> str:
    """
    Retrieves current timestamp in America/Sao_Paulo timezone

    Returns:
    ---------
    str: timestamp
    """
    return datetime.datetime.now(SAO_PAULO_TIMEZONE).isoformat(" ", "seconds")


def get_24_hours_from_now() -> datetime.datetime:
    """
    Returns a datetime.datetime object 24h from now

    Retuns:
    --------
    datetime.datetime
    """
    return datetime.datetime.now(SAO_PAULO_TIMEZONE) + datetime.timedelta(hours=24)
