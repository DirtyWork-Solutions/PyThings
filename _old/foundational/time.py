import datetime
from pytz import timezone as tz

class Time:
    """
    Represents a temporal concept.
    """
    def __init__(self, start_time, end_time, timezone: str = 'UTC'):
        self._parse_start = start_time if start_time else datetime.datetime.now()
        self._parse_stop = end_time if end_time else datetime.datetime.now()
        self.timezone = tz(timezone.upper())

    @property
    def duration(self):
        """
        :return: Duration between start and end.
        """
        fmt = '%Y-%m-%d'
        raise NotImplementedError()

    def overlaps(self, other) -> bool:
        """
        Check if this time period overlaps with another.
        :param other: (datetime *or* str) the other time
        :return: (bool) **True** if it does, else **False**.
        """
        # TODO: add logic for Temporal overlap check
        raise NotImplementedError(f"'overlaps' temporal is not implemented yet")

    def _parse_time(self):
        pass



    def __repr__(self):
        return f"Time({self._parse_start} to {self._parse_stop})"
