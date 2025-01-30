from typing import Any

from _old.entity.bases import BaseRelationship, BaseEntity

class Relationship(BaseRelationship):
    """
    Describes a relationship between entities.
    """
    def __init__(self, entity, rel_to, rel_type):
        self.name = rel_type if rel_type else 'relationship'
        self.entity_a: BaseEntity = entity
        self.entity_b: BaseEntity = rel_to
        self.verbose = 'is related to'

    def __str__(self):
        return f"{self.entity_a} {self.verbose} {self.entity_b}"

    def __repr__(self):
        return f"Relationship({self.entity_a, self.entity_b, self.name})"

    def validate(self, soft_check: bool = False) -> bool | None:
        """
        Perform validation checks on the relationship.
        :param soft_check: return a success boolean instead of raising an error.

        :return: boolean *or* nothing
        :raises ValueError: if both entities aren't present.
        """
        # Check for both entities
        if not self.entity_a or not self.entity_b:
            if soft_check:
                return False
            else:
                raise ValueError("Both entities must declared for a relationship.")

        # No checks failed, return True
        else:
            return True

class PartOf(Relationship):
    """
    Represents a **part-whole** relationship
    """
    def __init__(self, entity: BaseEntity, part_of: BaseEntity):
        """
        Initialise a *Part Of* relationship between two entities.
        :param entity: the entity instance.
        :param part_of: the entity it relates to.
        """
        super().__init__(entity, part_of, 'PartOf')


class SubclassOf(Relationship):
    """
    Represents a **subclass** relationship.
    """

    def __init__(self, entity: BaseEntity, sub_of: BaseEntity):
        super().__init__(entity, sub_of, 'SubclassOf')


class InstanceOf(Relationship):
    """
    Represents an **instance-of** relationship.
    """
    def __init__(self, entity: BaseEntity, instance_of: BaseEntity):
        super().__init__(entity, instance_of, 'InstanceOf')


class HasAttribute(Relationship):
    """
    Represents an **entity-attribute** relationship.
    """
    def __init__(self, entity: BaseEntity, attribute: BaseEntity):
        super().__init__(entity, attribute, 'HasAttribute')
        self.entity = entity
        self.attribute = attribute

class RelationshipManager:
    """
    Manages relationships between entities.
    """
    def __init__(self):
        self.relationships = []

    def add_relationship(self, relationship: Relationship):
        """
        Add a relationship to the manager
        :param relationship: the relationship instance
        :return: nothing
        """
        self.relationships.append(relationship)

    def find_relationships(self, entity: BaseEntity):
        """
        Find all relationships involving a specific entity.
        :param entity:
        :return: **list** of found relationships or **None**
        """
        found_results = []
        return found_results

    def determine_separation_degree(self, limit: int | None = 12):
        """
        Calculate the number of degrees of separation.

        E.g. A -> B -> D is 1 degree of separation between A and D.
        :param limit: give up after reaching a certain degree?
        :return: (int) number of degrees.
        """
        return 0