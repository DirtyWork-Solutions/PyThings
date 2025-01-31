import json
from abc import ABC, abstractmethod
from typing import Any, Dict
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

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseThing':
        pass

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data: str) -> 'BaseThing':
        return cls.from_dict(json.loads(data))


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

    def to_dict(self) -> Dict[str, Any]:
        return {
            'metadict': self._metadict.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Thing':
        instance = cls()
        instance._metadict = Metadata.from_dict(data['metadict'])
        return instance

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Thing):
            return False
        return self._metadict == other._metadict

    def __hash__(self) -> int:
        return hash(self._metadict)


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
        self.name = name
        self.value = value
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'value': self.value,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Attribute':
        return cls(
            name=data['name'],
            value=data['value'],
            description=data.get('description')
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Attribute):
            return False
        return (self.name, self.value, self.description) == (other.name, other.value, other.description)

    def __hash__(self) -> int:
        return hash((self.name, self.value, self.description))

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
            "uid": uid if uid is not None else uuid4()

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
        :return: (*dict*) metadata
        """
        return self._metadict

    def __getattr__(self, item):
        """
        Get an attribute of the metadata.
        :param item: metadata key.
        :return: Value of the metadata key.
        """
        keys = item.split('.')
        value = self._metadict
        for key in keys:
            value = value[key]
        return value

    def __repr__(self):
        """
        :return: (str) representation of the metadata.
        """
        return f"Metadata({self._metadict})"

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            'uid': str(self._metadict['uid']),
            'mappings': self._mappings
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Metadata':
        instance = cls(uid=data['uid'])
        instance._mappings = data['mappings']
        return instance

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Metadata):
            return False
        return self._metadict == other._metadict

    def __hash__(self) -> int:
        return hash(self._metadict['uid'])


class BaseRelationship(BaseThing):
    """
    Base class for all **relationship** classes.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize an instance of a **BaseRelationship**.
        """
        super().__init__()
        self.metadata = Metadata()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'metadata': self.metadata.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseRelationship':
        instance = cls()
        instance.metadata = Metadata.from_dict(data['metadata'])
        return instance

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseRelationship):
            return False
        return self.metadata == other.metadata

    def __hash__(self) -> int:
        return hash(self.metadata)


class Relationship(BaseRelationship):
    """
    Represents a *relationship* between **Things**.
    """

    def __init__(self):
        """
        Initialize an instance of a **Relationship**.
        """
        super().__init__()


class BaseInterface(ABC):
    """
    Base class for all **interfaces**.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize an instance of a **BaseInterface**.
        """
        pass

class Interface(BaseInterface):
    """
    Represents an *interface* for a **Thing**.
    """

    def __init__(self):
        """
        Initialize an instance of an **Interface**.
        """
        super().__init__()

if __name__ == '__main__':
    test = Metadata()
    print(test)