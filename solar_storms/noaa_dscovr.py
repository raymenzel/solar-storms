"""A data pipeline for NOAA DSCOVR realtime solar wind data."""

from datetime import datetime
from json import loads
from sqlite3 import IntegrityError

from flask import Flask
import requests

from .database import get_database_connection
from .data_pipeline import DataPipeline


default_url = "https://services.swpc.noaa.gov/products/geospace/" + \
              "propagated-solar-wind-1-hour.json"


class NoaaDscovrPipeline(DataPipeline):
    """A simple ETL (extract-transform-load) data pipeline for NOAA DSCOVR.
       The real-time solar wind data is updated every minute.

    Attributes:
        bad_records: List of record time_tags that are missing data.
        frequency: How often in seconds the data is updated at the source.
        column_names: List of data labels from the source.
        records: List of data records currently in memory.
    """
    def __init__(self):
        self.frequency = 60
        self.column_names = None
        self.records = None
        self.bad_records = []

    def extract(self, source=default_url, retention_period=24*60*60):
        """Gather data from the input source.

        Args:
            source: String source (in this case a url).
            retention_period: How long the data should be stored in
                              the database for.
        """
        request = requests.get(source)
        content = loads(request.content.decode("utf-8"))
        self.column_names = content[0] + ["retention_period",]
        self.records = [x + [retention_period,] for x in content[1:]]

    def transform(self):
        """Clean the source data before ingesting it into the database."""
        for record in self.records:
            for i, data in enumerate(record):
                if data is None and self.column_names[i] not in ["vx", "vy", "vz"]:
                    # Found a record that is missing needed data.
                    # Mark that this data needs to be re-downloaded.
                    self.bad_records.append(record[0])

    def load(self):
        """Store the data in the database."""
        database = get_database_connection()
        cursor = database.cursor()

        # Get the time of the most recent database entry.
        sql = "select time_tag from noaa_dscovr order by time_tag desc limit 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        try:
            last_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
        except TypeError:
            # The database is empty.  This is first time trying to add to it,
            # so just pick a time far in the past.
            last_time = datetime.strptime("1900-01-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
        time_tag_index = self.column_names.index("time_tag")

        for record in self.records:
            new_time = datetime.strptime(record[time_tag_index], "%Y-%m-%d %H:%M:%S.%f") 
            if record[0] in self.bad_records or new_time > last_time:
                # Update the database.
                names = ", ".join([name for name, value in zip(self.column_names, record)
                                   if value is not None])
                values = ", ".join([f"'{x}'" for x in record if x is not None])
                sql = f"insert into noaa_dscovr ({names}) values ({values})"
                try:
                    cursor.execute(sql)
                    if record[0] in self.bad_records:
                        # The bad record has been fixed and correctly inserted
                        # into the database.
                        self.bad_records.remove(record[0])
                except IntegrityError:
                    if record[0] not in self.bad_records:
                        self.bad_records.append(record[0])
        database.commit()
        self.column_names = None
        self.records = None

    def prune(self, application: Flask):
        """Remove stale data from the database.

        Args:
            application: The flask application.
        """
        raise NotImplementedError("this is not implemented yet.")

    def execute(self, application: Flask):
        """Run through the entire pipeline.

        Args:
            application: The flask application.
        """
        self.extract()
        self.transform()
        with application.app_context():
            self.load()
