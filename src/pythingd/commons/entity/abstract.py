"""
TODO: Package docs
"""

from typing import Any, List

from src.pythingd.__base__ import BaseAttribute, BaseAbstractEntity


class AbstractEntity(BaseAbstractEntity):
    """
    Base class for all abstract entities.
    """
    def __init__(self, name: str = 'unknown abstract entity'):
        """
        # TODO: method docs

        :param name:
        """
        self.name = name


class Attribute(BaseAttribute):
    """
    Represents an attribute of an entity.
    """
    def __init__(self, name: str = 'attribute', value: Any = None):
        """
        TODO: method docs

        :param name:
        :param value:
        """
        super().__init__(name)
        self.value = value


class Set(AbstractEntity):
    """
    Represents a collection or group of entities.
    """
    def __init__(self, name: str = 'unknown set', members: List = None):
        """
        TODO: Method docs

        :param name:
        :param members:
        """
        super().__init__(name)
        self.members = members if members else []

    def add_member(self, new_member):
        """
        Add a member to the set.

        :param new_member:
        :return: nothing
        """
        self.members.append(new_member)


    def remove_member(self):
        """
        Remove a member from the collection/set.

        :return:
        """
        raise NotImplementedError()

    def __repr__(self):
        return f"Set({self.name}): {self.members}"


