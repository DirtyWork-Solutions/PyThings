"""
TODO: Module docs
"""
from abc import ABC, abstractmethod

from pythings.commons.entity.abstract import BaseAbstractEntity
from pythings.__base__ import BaseEntity


class BaseRelationship(BaseAbstractEntity, ABC):
    """
    Base class for all relationship classes.
    """

    @abstractmethod
    def __init__(self):
        """
        TODO: Method docs
        """
        super().__init__()

        #
        pass

    def __repr__(self):
        return f"Relationship()"


class Relationship(BaseRelationship):
    """
    Describes a relationship between entities.
    """

    def __init__(self, entity, rel_to, rel_type):
        """
        TODO: Method docs

        :param entity:
        :param rel_to:
        :param rel_type:
        """
        # Set relationship properties
        self.name = rel_type if rel_type else 'relationship'  # TODO: Move/Integrate with meta?
        self.entity_a: BaseEntity = entity
        self.entity_b: BaseEntity = rel_to
        self.verbose = 'is related to'

    def __str__(self):
        return f"{self.entity_a} {self.verbose} {self.entity_b}"

    def __repr__(self):
        return f"Relationship({self.entity_a, self.entity_b, self.name})"
