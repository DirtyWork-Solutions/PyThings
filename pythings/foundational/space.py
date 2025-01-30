from pythings.base import FoundationalThing
from pythings.commons.entity import BaseEntity


class SpatialThing(BaseEntity, FoundationalThing):
    """
    Represents a spatial entity.
    """
    def __init__(self, name: str = 'unknown entity'):
        """

        :param name:
        """
        super().__init__()