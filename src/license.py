"""
Flying licence module
"""
import os
from random import sample
from string import digits
from src import database

MINIMUM_FLYING_HOURS = os.getenv("MINIMUM_FLYING_HOURS")
if MINIMUM_FLYING_HOURS is None:
    raise RuntimeError("Couldn't find MINIMUM_FLYING_HOURS in env variable")
MINIMUM_FLYING_HOURS = int(MINIMUM_FLYING_HOURS)


def can_issue(student_id: str) -> bool:
    """
    Calculates whether student can have her/his licence issued.

    For a licence to be issued, the student must have completed at least the MINIMUM_FLYING_HOURS.
    Moreover, at least 85% of the flying hours must have grades 3 or 4.

    Params:
    -------
    student_id: str
        Student document

    Returns:
    --------
    bool: whether student can have her/his licence issued
    """
    student_flights = database.get_documents(
        "flights", {"student_id": student_id})

    total_flying_hours = sum(
        [flight["duration"] for flight in student_flights])

    if total_flying_hours < MINIMUM_FLYING_HOURS:
        return False

    high_grade_flying_hours = sum(
        [flight["duration"] for flight in student_flights if flight["grade"] in (3, 4)])

    if high_grade_flying_hours / MINIMUM_FLYING_HOURS < .85:
        return False

    return True


def issue() -> str:
    """
    Issues a 10-digit licence number.

    Returns:
    --------
    str: licence number
    """
    return "".join(sample(digits, 10))
