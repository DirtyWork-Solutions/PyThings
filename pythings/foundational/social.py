from pythings.base import FoundationalThing, BaseRelationship


class BaseSocialThing(FoundationalThing):
    """
    Represents a social entity.
    """
    def __init__(self, name: str = 'unknown entity'):
        """

        :param name:
        """
        super().__init__()

class SocialThing(BaseSocialThing):
    """
    Represents a social entity.
    """
    def __init__(self, name: str = 'unknown entity'):
        """

        :param name:
        """
        super().__init__(name)

class SocialRelationship(BaseSocialThing, BaseRelationship):
    """
    Represents a social relationship.
    """
    def __init__(self, name: str = 'unknown relationship'):
        """

        :param name:
        """
        super().__init__(name)