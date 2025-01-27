from typing import Any

from entity.bases import BaseRelationship, BaseEntity

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

