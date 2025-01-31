from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID, uuid4

"""
Base classes and abstractions.
"""

class BaseThing(ABC):
    """
    Base class for all **Things**.

    A *Thing* is a generic abstraction for anything, composable by default.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialise an instance of a **Thing**.
        """
        pass


class Thing(BaseThing):
    """
    A generic abstraction for anything, composable by default.
    """

    def __init__(self):
        """
        Initialise an instance of a **Thing**.
        """
        super().__init__()
        self._metadict = Metadata()


class FoundationalThing(Thing):
    """
    A foundational **Thing**.  # TODO: Improve these docs
    """

    def __init__(self):
        super().__init__()


class Attribute(BaseThing):
    """
    A generic abstraction for an *attribute* of a **Thing**.
    """

    def __init__(self, name: str, value: Any, description: str = None):
        super().__init__()

class Metadata(BaseThing):
    """
    A generic abstraction for *metadata* of a **Thing**.
    """

    def __init__(self, uid: UUID | str | None = None):
        """
        Initialise an instance of **Metadata**.
        :param uid:
        """
        super().__init__()
        self._metadict = {
            "uuid": uid if uid is not None else uuid4()

        }
        self._mappings = {
            "sql": None,
            "neo4j": None,
            "sumo": None

        }

    @property
    def metadata(self):
        """
        Get the metadata.
        :return: (dict) metadata
        """
        return self._metadict

    def __getattr__(self, item):
        """
        Get an attribute of the metadata.
        :param item: metadata key.
        :return:
        """
        keys = item.split('.')
        value = self._metadict
        for key in keys:
            value = value[key]
        return value

    def __setattr__(self, key, value):
        """
        Set an attribute of the metadata.
        :param key: metadata key.
        :param value: metadata value.
        :return:
        """
        try:
            self._metadict[key] = value
        except KeyError as e:
            raise e
        finally:  # TODO Audit/Event logic here
            pass

    def get_mappings(self):
        """
        Get all the mappings for *Metadata*.
        :return: (dict) mappings
        """
        return self._mappings

    @property
    def mappings(self):
        """
        :return: (dict) Metadata mappings.
        """
        return self.get_mappings()


class BaseRelationship(BaseThing):
    """
    Base class for all **relationship** classes.
    """

    @abstractmethod
    def __init__(self):
        """

        """
        super().__init__()
        self.metadata = Metadata()


class Relationship(BaseRelationship):
    """
    Represents a *relationship* between **Things**.
    """

    def __init__(self):
        """

        """
        super().__init__()



if __name__ == '__main__':
    test = Metadata()
    print(test)