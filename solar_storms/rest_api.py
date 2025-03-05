"""Provides a REST API for the solar wind data."""

from flask import Blueprint, current_app, request
from flask_restful import abort, reqparse, Resource

from .database import get_database_connection


api_blueprint = Blueprint("api", __name__)
solar_wind_parser = reqparse.RequestParser()
#solar_wind_parser.add_argument()


class NoaaDscovr(Resource):
    def get(self):
        args = solar_wind_parser.parse_args()
        database = get_database_connection()
        cursor = database.cursor()
        sql = "select * from noaa_dscovr"
        cursor.execute(sql)
        result = cursor.fetchmany()
        response = {}
        for record in result:
            response[record[0]] = [record[1:]]
        return response
