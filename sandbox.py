from typing import Any, Dict, List, Optional


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
                 label: Optional[str] = None,
                 description: str = "",
                 sumo_class: str = "Entity"):
        self._identifier = identifier
        self.label = label if label is not None else identifier
        self.description = description
        self.sumo_class = sumo_class

        # Instead of embedding raw dicts, store lists of related objects.
        self._attributes: List[Attribute] = []
        self._relationships: List[Relationship] = []

        self._incoming_relationships: List['Relationship'] = []


    @property
    def identifier(self) -> str:
        return self._identifier

    def __eq__(self, other: Any) -> bool:  # TODO: Think this other
        return isinstance(other, BaseEntity) and self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


    def add_attribute(self, attribute: 'Attribute') -> None:
        """Associates an Attribute object with this entity."""
        if attribute not in self._attributes:
            self._attributes.append(attribute)

    def remove_attribute(self, attribute: 'Attribute') -> None:  # TODO: Allow for removing via ID or Name
        """Removes an Attribute associated with this entity."""
        self._attributes = [attr for attr in self._attributes if attr != attribute]

    def get_attributes(self) -> List['Attribute']:
        """Returns all associated Attribute objects."""
        return self._attributes

    def add_relationship(self, relationship: 'Relationship') -> None:
        """Associates a Relationship object with this entity."""
        if relationship not in self._relationships:
            self._relationships.append(relationship)

    def remove_relationship(self, relationship: 'Relationship') -> None:  # TODO: Method docs
        self._relationships = [rel for rel in self._relationships if rel != relationship]

    def add_incoming_relationship(self, relationship: 'Relationship') -> None:  # TODO: Method docs
        if relationship not in self._incoming_relationships:
            self._incoming_relationships.append(relationship)

    def get_incoming_relationships(self, relation_type: Optional[str] = None) -> List[
        'Relationship']:  # TODO: Method docs
        if relation_type is None:
            return self._incoming_relationships
        return [rel for rel in self._incoming_relationships if rel.relation_type == relation_type]

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

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        """Serializes the entity and its related attributes/relationships to a dictionary."""
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

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        base = super().to_dict(recursive)
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
        self.target.add_incoming_relationship(self)

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        base = super().to_dict(recursive)
        base.update({
            "source": self.source.identifier,
            "relation_type": self.relation_type,
            "target": self.target.identifier
        })
        return base


class EntityGraph:
    def __init__(self) -> None:
        self.entities: Dict[str, BaseEntity] = {}

    def add_entity(self, entity: BaseEntity) -> None:
        self.entities[entity.identifier] = entity

    def get_entity(self, identifier: str) -> Optional[BaseEntity]:
        return self.entities.get(identifier)

    def find_relationships(self, relation_type: Optional[str] = None) -> List[Relationship]:
        rels = []
        for entity in self.entities.values():
            rels.extend(entity.get_relationships(relation_type))
        return rels


# Example usage:
if __name__ == "__main__":
    # Create an entity graph.
    graph = EntityGraph()

    # Create some basic entities.
    e1 = BaseEntity("E1", label="Entity One", description="A basic entity.")
    e2 = BaseEntity("E2", label="Entity Two")

    graph.add_entity(e1)
    graph.add_entity(e2)

    # Create a relationship between e1 and e2.
    rel = Relationship("R1", source=e1, relation_type="related_to", target=e2, label="Relationship One")

    # Create an attribute for e1.
    attr = Attribute("A1", domain=e1, name="color", value="red", label="Color Attribute")

    # Print serialized output.
    print(e1.to_dict())
    print(graph.entities)
