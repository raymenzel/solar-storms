from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api

from .database import get_database_connection, initialize_application
from .noaa_dscovr import NoaaDscovrPipeline
from .rest_api import api_blueprint, NoaaDscovr
from .routes import solar_storms_blueprint


scheduler = APScheduler()  # Scheduler for recurring tasks.
noaa_dscovr_pipeline = NoaaDscovrPipeline()  # Data pipeline.


def create_app() -> Flask:
    """Create the flask application."""
    application = Flask(__name__)
    initialize_application(application)

    # Configure the application.
    application.config["APS_JOBSTORES"] = {
        "default": {"type": "memory"},
    }
    application.config["APS_SCHEDULER_API_ENABLED"] = True

    # Schedule recurring tasks.
    scheduler.init_app(application)
    scheduler.add_job(
        func=noaa_dscovr_pipeline.execute,
        trigger="interval",
        seconds=noaa_dscovr_pipeline.frequency,
        args=[application],
        id="execute_noaa_dscovr_pipeline",
    )
    scheduler.start()

    # Add the routes.
    application.register_blueprint(solar_storms_blueprint)

    # Add the rest api.
    api = Api(application)
    api.add_resource(NoaaDscovr, "/api/solar-wind")
    application.register_blueprint(api_blueprint)
    return application
