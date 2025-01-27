import datetime


class Time:
    """
    Represents a temporal concept.
    """
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime.now()
        self.stop: datetime.datetime = datetime.datetime.now()

    @property
    def duration(self):
        """
        :return: Duration between start and end.
        """
        fmt = '%Y-%m-%d'
        raise NotImplementedError()

    def __repr__(self):
        return f"Time({self.start} to {self.stop})"
