from pythings.base import FoundationalThing, Relationship, Attribute

class SpatialThing(FoundationalThing):
    """
    Represents a spatial entity.
    """
    def __init__(self, name: str = 'unknown entity'):
        """

        :param name:
        """
        super().__init__()