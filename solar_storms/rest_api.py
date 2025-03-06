"""Provides a REST API for the solar wind data."""

from datetime import datetime

from flask import Blueprint, current_app, request
from flask_restful import abort, reqparse, Resource

from .database import get_database_connection


api_blueprint = Blueprint("api", __name__)

# Arguments that you can pass in.
solar_wind_parser = reqparse.RequestParser()
solar_wind_parser.add_argument(
    "time_begin",
    required=False,
    help="Beginning of a time range in YYYY-mm-dd_HH:MM:SS",
    location="args"
)
solar_wind_parser.add_argument(
    "time_end",
    required=False,
    help="End of a time range in YYYY-mm-dd_HH:MM:SS",
    location="args"
)

def fix_date_string(string_in):
    string_date = string_in.replace("_", " ")
    return datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")


class NoaaDscovr(Resource):
    def get(self):
        args = solar_wind_parser.parse_args()
        sql = "select * from noaa_dscovr"
        conditions = []
        if args["time_begin"]:
            begin_time = fix_date_string(args["time_begin"])
            conditions.append(f"time_tag >= '{begin_time}'")
        if args["time_end"]:
            end_time = fix_date_string(args["time_end"])
            conditions.append(f"time_tag <= '{end_time}'")
        if conditions:
            sql += " where " + " and ".join(conditions)

        database = get_database_connection()
        cursor = database.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        response = {}
        for record in result:
            data = {key: record[i + 1] for i, key in enumerate(record.keys()[1:])}
            response[record[0]] = data
        return response
