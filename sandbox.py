from typing import Any, Dict, List


class BaseEntity:
    """
    Represents a basic entity in the system with core properties shared across all entities.

    Attributes:
        identifier (str): A unique identifier.
        label (str): A human-readable label (defaults to the identifier if not provided).
        description (str): A textual description.
        sumo_class (str): The SUMO class name, by default "Entity".
    """

    def __init__(self,
                 identifier: str,
                 label: str = None,
                 description: str = "",
                 sumo_class: str = "Entity"):
        self.identifier = identifier
        self.label = label if label is not None else identifier
        self.description = description
        self.sumo_class = sumo_class

        # Instead of embedding raw dicts, store lists of related objects.
        self._attributes: List[Attribute] = []
        self._relationships: List[Relationship] = []

    def add_attribute(self, attribute: 'Attribute') -> None:
        """Associates an Attribute object with this entity."""
        self._attributes.append(attribute)

    def get_attributes(self) -> List['Attribute']:
        """Returns all associated Attribute objects."""
        return self._attributes

    def add_relationship(self, relationship: 'Relationship') -> None:
        """Associates a Relationship object with this entity."""
        self._relationships.append(relationship)

    def get_relationships(self, relation_type: str = None) -> List['Relationship']:
        """
        Returns associated Relationship objects.

        Args:
            relation_type (str, optional): If provided, filters relationships by their type.
        """
        if relation_type is None:
            return self._relationships
        else:
            return [rel for rel in self._relationships if rel.relation_type == relation_type]

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the entity and its related attributes/relationships to a dictionary."""
        return {
            "identifier": self.identifier,
            "label": self.label,
            "description": self.description,
            "sumo_class": self.sumo_class,
            "attributes": [attr.to_dict() for attr in self._attributes],
            "relationships": [rel.to_dict() for rel in self._relationships]
        }

    def __repr__(self) -> str:
        return f"<{self.sumo_class}: {self.label} ({self.identifier})>"


class Attribute(BaseEntity):
    """
    Represents an Attribute as an entity in its own right.

    In SUMO, attributes can have their own relationships and properties.

    Attributes:
        domain (BaseEntity): The entity that this attribute describes.
        name (str): The attribute's name.
        value (Any): The value associated with the attribute.
    """

    def __init__(self,
                 identifier: str,
                 domain: BaseEntity,
                 name: str,
                 value: Any,
                 label: str = None,
                 description: str = ""):
        super().__init__(identifier, label, description, sumo_class="Attribute")
        self.domain = domain
        self.name = name
        self.value = value

        # Optionally register this attribute with its domain entity.
        self.domain.add_attribute(self)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "domain": self.domain.identifier,
            "name": self.name,
            "value": self.value
        })
        return base


class Relationship(BaseEntity):
    """
    Represents a Relationship as an entity, aligning with SUMO's treatment of relationships.

    Attributes:
        source (BaseEntity): The entity from which the relationship originates.
        relation_type (str): The type or nature of the relationship.
        target (BaseEntity): The entity at the receiving end of the relationship.
    """

    def __init__(self,
                 identifier: str,
                 source: BaseEntity,
                 relation_type: str,
                 target: BaseEntity,
                 label: str = None,
                 description: str = ""):
        super().__init__(identifier, label, description, sumo_class="Relationship")
        self.source = source
        self.relation_type = relation_type
        self.target = target

        # Optionally register this relationship with the source entity.
        self.source.add_relationship(self)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "source": self.source.identifier,
            "relation_type": self.relation_type,
            "target": self.target.identifier
        })
        return base


# Example usage:
if __name__ == "__main__":
    # Create some basic entities.
    e1 = BaseEntity("E1", label="Entity One", description="A basic entity.")
    e2 = BaseEntity("E2", label="Entity Two")

    # Create a relationship between e1 and e2.
    rel = Relationship("R1", source=e1, relation_type="related_to", target=e2, label="Relationship One")

    # Create an attribute for e1.
    attr = Attribute("A1", domain=e1, name="color", value="red", label="Color Attribute")

    # Print serialized output.
    print(e1.to_dict())
    print(e2.get_relationships())
    print(e1.get_relationships())
