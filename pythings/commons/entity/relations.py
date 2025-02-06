"""
TODO: Module docs
"""
from typing import Optional

from pythings.__base__ import BaseEntity, Entity, BaseAttribute, BaseAbstractEntity, BasePhysicalEntity, \
    BaseRelationship

class Relationship(BaseRelationship):
    """
    Describes a relationship between entities.
    """

    def __init__(self,
                 identifier: str,
                 source: BaseEntity,
                 relation_type: str,
                 target: BaseEntity,
                 label: Optional[str] = None,
                 description: str = "") -> None:
        super().__init__(identifier, label, description)
        self.source: BaseEntity = source
        self.relation_type: str = relation_type
        self.target: BaseEntity = target

        # Add relationship to source and target entities
        self.source.add_relationship(self)
        self.target.add_incoming_relationship(self)
