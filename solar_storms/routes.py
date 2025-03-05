from flask import Blueprint

from .database import get_database_connection


solar_storms_blueprint = Blueprint("solar_storms", __name__)


@solar_storms_blueprint.route("/")
def index() -> str:
    return "<p>Dashboard coming soon</p>"
