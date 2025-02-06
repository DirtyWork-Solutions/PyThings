"""
TODO: root module docs
"""

import logging as logger

from abc import abstractmethod, ABC
from typing import Dict, Any, Optional, List


class BaseEntity(ABC):
    """
    Represents a basic entity in the system with core properties shared across all entities.

    Attributes:
        identifier (str): A unique identifier.
        label (str): A human-readable label (defaults to the identifier if not provided).
        description (str): A textual description.
        sumo_class (str): The SUMO class name, by default "Entity".
    """

    @abstractmethod
    def __init__(self,
                 identifier: str,
                 label: Optional[str] = None,
                 description: str = "",
                 sumo_class: str = "Entity") -> None:
        self._identifier = identifier
        self.label: str = label if label is not None else identifier
        self.description: str = description
        self.sumo_class: str = sumo_class
        self._attributes: List['BaseAttribute'] = []
        self._relationships: List['BaseRelationship'] = []
        self._incoming_relationships: List['BaseRelationship'] = []

    @property
    def identifier(self) -> str:
        return self._identifier

    def add_attribute(self, attribute: 'BaseAttribute') -> None:
        if attribute not in self._attributes:
            self._attributes.append(attribute)
            logger.debug(f"Added attribute {attribute.identifier} to entity {self.identifier}")

    def remove_attribute(self, attribute: 'BaseAttribute') -> None:
        self._attributes = [attr for attr in self._attributes if attr != attribute]

    def get_attributes(self) -> List['BaseAttribute']:
        return self._attributes

    def add_relationship(self, relationship: 'BaseRelationship') -> None:
        if relationship not in self._relationships:
            self._relationships.append(relationship)
            logger.debug(f"Added relationship {relationship.identifier} to entity {self.identifier}")

    def remove_relationship(self, relationship: 'BaseRelationship') -> None:
        self._relationships = [rel for rel in self._relationships if rel != relationship]

    def add_incoming_relationship(self, relationship: 'BaseRelationship') -> None:
        if relationship not in self._incoming_relationships:
            self._incoming_relationships.append(relationship)
            logger.debug(f"Added incoming relationship {relationship.identifier} to entity {self.identifier}")

    def get_relationships(self, relation_type: Optional[str] = None) -> List['BaseRelationship']:
        if relation_type is None:
            return self._relationships
        return [rel for rel in self._relationships if rel.relation_type == relation_type]

    def get_incoming_relationships(self, relation_type: Optional[str] = None) -> List['BaseRelationship']:
        if relation_type is None:
            return self._incoming_relationships
        return [rel for rel in self._incoming_relationships if rel.relation_type == relation_type]

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        base = {
            "identifier": self.identifier,
            "label": self.label,
            "description": self.description,
            "sumo_class": self.sumo_class,
        }
        if recursive:
            base["attributes"] = [attr.to_dict(recursive=False) for attr in self._attributes]
            base["relationships"] = [rel.to_dict(recursive=False) for rel in self._relationships]
        else:
            base["attributes"] = [attr.identifier for attr in self._attributes]
            base["relationships"] = [rel.identifier for rel in self._relationships]
        return base

    def __repr__(self) -> str:
        return f"<{self.sumo_class}: {self.label} ({self.identifier})>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BaseEntity) and self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


class BaseAbstractEntity(BaseEntity, ABC):

    @abstractmethod
    def __init__(self,
                 identifier: str,
                 label: Optional[str] = None,
                 description: str = "",
                 sumo_class: str = "AbstractEntity") -> None:
        super().__init__(identifier, label, description, sumo_class)


class BasePhysicalEntity(BaseEntity, ABC):

    @abstractmethod
    def __init__(self,
                 identifier: str,
                 label: Optional[str] = None,
                 description: str = "",
                 sumo_class: str = "PhysicalEntity") -> None:
        super().__init__(identifier, label, description, sumo_class)


class Entity(BaseEntity):

    @abstractmethod
    def __init__(self,
                 identifier: str,
                 label: Optional[str] = None,
                 description: str = "",
                 sumo_class: str = "Entity") -> None:
        super().__init__(identifier, label, description, sumo_class)


class BaseAttribute(BaseEntity, ABC):
    """
    Represents an Attribute as an entity in its own right.
    """

    @abstractmethod
    def __init__(self,
                 identifier: str,
                 domain: BaseEntity,
                 name: str,
                 value: Any,
                 label: Optional[str] = None,
                 description: str = "") -> None:
        super().__init__(identifier, label, description, sumo_class="Attribute")
        self.domain: BaseEntity = domain
        self.name: str = name
        self.value: Any = value
        self.domain.add_attribute(self)

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        base = super().to_dict(recursive)
        base.update({
            "domain": self.domain.identifier,
            "name": self.name,
            "value": self.value
        })
        return base


class BaseRelationship(BaseEntity, ABC):
    """
    Represents a Relationship as an entity.
    """

    @abstractmethod
    def __init__(self,
                 identifier: str,
                 source: BaseEntity,
                 relation_type: str,
                 target: BaseEntity,
                 label: Optional[str] = None,
                 description: str = "") -> None:
        super().__init__(identifier, label, description, sumo_class="Relationship")
        self.source: BaseEntity = source
        self.relation_type: str = relation_type
        self.target: BaseEntity = target

        # Add relationship to source and target entities
        self.source.add_relationship(self)
        self.target.add_incoming_relationship(self)

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        base = super().to_dict(recursive)
        base.update({
            "source": self.source.identifier,
            "relation_type": self.relation_type,
            "target": self.target.identifier
        })
        return base
