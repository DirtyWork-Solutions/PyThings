from abc import ABC, abstractmethod

from foundational.time import Time

class BaseEntity(ABC):
    """
    Base class for all entity classes.
    """
    @abstractmethod
    def __init__(self):
        pass

class BaseRelationship(ABC):
    """
    Base class for all relationship classes.
    """
    @abstractmethod
    def __init__(self):
        pass