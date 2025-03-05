"""Defines an abstract class to create data pipelines to different sources."""


class DataPipeline(object):
    """Abstract base class that can be extended to different data sources."""
    def __init__(self):
        raise NotImplementedError("this must be overridden.")

    def extract(self, source):
        """Gathers the data from the data source.

        Args:
            source: The source of the data (i.e., url, file, etc.).
        """
        raise NotImplementedError("this must be overridden.")

    def transform(self):
        """Cleans up the data and transforms the data to meet the application schema."""
        raise NotImplementedError("this must be overridden.")

    def load(self):
        """Loads the data into the application database."""
        raise NotImplementedError("this must be overridden.")
