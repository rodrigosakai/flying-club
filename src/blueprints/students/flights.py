"""
Flights blueprint
"""
from flask import Blueprint, request
from src import auth, database
from src.auth import UserRole


flights_bp = Blueprint("flights_bp", __name__)


@flights_bp.route("/<string:student_id>", methods=["POST"])
@auth.validate_auth([UserRole.INSTRUCTOR])
def register_flight(student_id):
    pass
