from datetime import datetime

from pythings.__base__ import BaseEntity, Entity, BaseAttribute, BaseAbstractEntity, BasePhysicalEntity, \
    BaseRelationship

class Time:
    """
    Represents a temporal concept.
    """

    def __init__(self):
        """
        TODO: Method docs
        """
        self.start: datetime = datetime.now()
        self.stop: datetime = datetime.now()

    @property
    def duration(self):  # TODO: Fully implement method
        """
        TODO: Method docs

        :return: Duration between start and end.
        """
        fmt = '%Y-%m-%d'
        raise NotImplementedError()

    def __repr__(self):
        return f"Time({self.start} to {self.stop})"
