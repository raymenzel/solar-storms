"""Helper functions that control the application database."""

from os import getenv
from sqlite3 import connect, Connection, PARSE_DECLTYPES, Row

from click import command, echo
from flask import current_app, Flask, g


def get_database_connection() -> Connection:
    """Connects to and retrieves the database.

    Returns:
        sqlite3 Connection to the database.
    """
    if "database" not in g:
        path = getenv("SOLAR_STORMS_DATABASE")
        if path is None:
            raise ValueError("Please set the SOLAR_STORMS_DATABASE environment variable.")
        g.database = connect(path, detect_types=PARSE_DECLTYPES)
        g.database.row_factory = Row
    return g.database


def close_database_connection(e=None) -> None:
    """Closes the database connection.

    Args:
        e: not used.
    """
    database = g.pop("db", None)
    if database is not None:
        database.close()


def initialize_application(application: Flask) -> None:
    """Initializes the flask application.

    Args:
        application: Flask application object.
    """
    application.teardown_appcontext(close_database_connection)
    application.cli.add_command(initialize_database_command)


def initialize_database() -> None:
    """Inititalizes the database."""
    database = get_database_connection()
    with current_app.open_resource("schema.sql") as file_:
        database.executescript(file_.read().decode("utf8"))


@command("init-db")
def initialize_database_command() -> None:
    """Runs when the init-db command line option is used."""
    initialize_database()
    echo("Initialized the database.")
