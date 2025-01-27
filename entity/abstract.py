from typing import Any, List

from entity.bases import BaseEntity


class AbstractEntity(BaseEntity):
    """
    Base class for all abstract entities.
    """
    def __init__(self, name: str = 'unknown abstract entity'):
        self.name = name

class Attribute(AbstractEntity):
    """
    Represents an attribute of an entity.
    """
    def __init__(self, name: str = 'attribute', value: Any = None):
        super().__init__(name)
        self.value = value

class Set(AbstractEntity):
    """
    Represents a collection or group of entities.
    """
    def __init__(self, name: str = 'unknown set', members: List = None):
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
        raise NotImplementedError()

    def __repr__(self):
        return f"Set({self.name}): {self.members}"
