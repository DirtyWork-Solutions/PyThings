from abc import ABC, abstractmethod
from uuid import UUID, uuid4

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

class Thing:
    """
    A generic abstraction for anything, composable by default.
    """

    def __init__(self,
                 name: str | None = None,
                 uid: UUID | str | None = None,
                 attributes: dict | list | None = None,
                 metadata: dict | None = None):
        """
        Initialise an instance of a Thing.
        :param name:
        :param uid:
        :param attributes:
        :param metadata:
        """
        # Set default properties
        self.name = name if name else 'unknown thing'
        self.uuid = uid if uid else str(uuid4())
        self._attributes = attributes if attributes else []
        self._metadata = metadata if metadata else {}

