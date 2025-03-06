from json import loads
from os import environ
from pathlib import Path

import pytest
import requests
from solar_storms import create_app


@pytest.fixture()
def app():
    database = Path(__file__).resolve().parent / "test.db"
    environ["SOLAR_STORMS_DATABASE"] = str(database)
    application = create_app()
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_rest_api(client):
    request = client.get("/api/solar-wind")
    content = loads(request.data.decode("utf-8").strip())
    expected_keys = ['time_tag', 'speed', 'density', 'temperature', 'bx',
                     'by', 'bz', 'bt', 'vx', 'vy', 'vz', 'propagated_time_tag',
                     'retention_period']
    for entry in content.values():
        for key in entry.keys():
            if key not in expected_keys:
                raise ValueError(f"unexpected key {key}.")
