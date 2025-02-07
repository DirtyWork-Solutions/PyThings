"""
Module: relations.py

This module enhances relationship functionality in PyThings by introducing a concrete
implementation of the BaseRelationship class. It leverages SUMO standards for semantic clarity,
introduces type-safe relationship types via an Enum, and supports enhanced (recursive)
serialization of relationship data.
"""

from typing import Any, Dict, Optional, List
from enum import Enum
import json
import xml.etree.ElementTree as ET

import networkx as nx

from pythings.__base__ import BaseEntity, Entity, BaseAttribute, BaseAbstractEntity, BasePhysicalEntity, \
    BaseRelationship


class RelationType(Enum):
    """
    Enumeration of standard relationship types based on SUMO (Suggested Upper Merged Ontology)
    concepts. Each member includes a value and a human-readable description.
    """
    PART_OF = ("partOf", "Indicates that an entity is a component or sub-part of another.")
    ASSOCIATED_WITH = ("associatedWith", "Indicates a general link or connection between entities.")
    RELATED_TO = ("relatedTo", "Indicates that there is some form of relationship or connection between entities.")
    DEPENDS_ON = ("dependsOn", "Indicates that an entity's existence or functionality relies on another.")

    def __init__(self, value: str, description: str):
        self._value_ = value
        self.description = description

    @classmethod
    def from_value(cls, value: str) -> "RelationType":
        """
        Returns the RelationType corresponding to the given string value.
        Raises ValueError if the value does not match any RelationType.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' is not a valid RelationType.")

    def __str__(self):
        return self.value


class StandardRelationship(BaseRelationship):
    """
    StandardRelationship is a concrete implementation of BaseRelationship.

    It represents a directed relationship between two entities, ensuring that the relationship
    is registered with both the source and target entities. It also supports enhanced serialization,
    optionally embedding more details from linked entities.
    """

    def __init__(self,
                 identifier: str,
                 source: BaseEntity,
                 relation_type: RelationType,
                 target: BaseEntity,
                 label: Optional[str] = None,
                 description: str = "",
                 sumo_class: Optional[str] = None) -> None:
        # Relationship Validation: Prevent self-referencing relationships.
        if source.identifier == target.identifier:
            raise ValueError("Source and target entities must be distinct.")

        # Additional domain-specific validations can be added here.
        sumo_class_value = sumo_class if sumo_class is not None else "Relationship"
        # Note: BaseRelationship expects the relation_type as a string.
        super().__init__(identifier, source, relation_type.value, target, label, description)
        self.sumo_class = sumo_class_value

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        base = super().to_dict(recursive)
        if recursive and hasattr(self.source, "to_dict"):
            source_repr = self.source.to_dict(recursive=False)
        else:
            source_repr = self.source.identifier

        if recursive and hasattr(self.target, "to_dict"):
            target_repr = self.target.to_dict(recursive=False)
        else:
            target_repr = self.target.identifier

        base.update({
            "source": source_repr,
            "relation_type": self.relation_type,
            "target": target_repr,
            "sumo_class": self.sumo_class
        })
        return base

    def to_json(self, recursive: bool = True) -> str:
        """
        Returns a JSON representation of the relationship.
        """
        return json.dumps(self.to_dict(recursive), indent=2)

    def to_xml(self, recursive: bool = True) -> str:
        """
        Returns an XML string representation of the relationship.
        """
        relationship_dict = self.to_dict(recursive)
        root = ET.Element("Relationship")
        for key, value in relationship_dict.items():
            # For nested dictionaries, create subelements
            if isinstance(value, dict):
                sub_elem = ET.SubElement(root, key)
                for sub_key, sub_value in value.items():
                    child = ET.SubElement(sub_elem, sub_key)
                    child.text = str(sub_value)
            else:
                elem = ET.SubElement(root, key)
                elem.text = str(value)
        return ET.tostring(root, encoding="unicode")


class RelationshipManager:
    """
    Manages relationships and provides bidirectional navigation between entities.
    """

    def __init__(self):
        self.relationships: List[StandardRelationship] = []

    def add_relationship(self, relationship: StandardRelationship) -> None:
        self.relationships.append(relationship)

    def get_relationships_from(self, source: BaseEntity) -> List[StandardRelationship]:
        """
        Returns all relationships where the given entity is the source.
        """
        return [rel for rel in self.relationships if rel.source.identifier == source.identifier]

    def get_relationships_to(self, target: BaseEntity) -> List[StandardRelationship]:
        """
        Returns all relationships where the given entity is the target.
        """
        return [rel for rel in self.relationships if rel.target.identifier == target.identifier]

    def get_all_relationships(self) -> List[StandardRelationship]:
        return self.relationships


class RelationshipBulkManager:
    """
    Handles bulk operations for relationships.
    """

    def __init__(self, relationship_manager: RelationshipManager):
        self.manager = relationship_manager

    def create_bulk(self, relationships_data: List[Dict[str, Any]]) -> List[StandardRelationship]:
        """
        Create multiple relationships in bulk.
        Each dictionary in relationships_data should contain the keys required to instantiate a StandardRelationship.
        """
        created_relationships = []
        for data in relationships_data:
            relationship = StandardRelationship(
                identifier=data["identifier"],
                source=data["source"],
                relation_type=data["relation_type"],
                target=data["target"],
                label=data.get("label"),
                description=data.get("description", ""),
                sumo_class=data.get("sumo_class")
            )
            self.manager.add_relationship(relationship)
            created_relationships.append(relationship)
        return created_relationships

    def delete_bulk(self, identifiers: List[str]) -> None:
        """
        Delete relationships in bulk by their identifiers.
        """
        self.manager.relationships = [
            rel for rel in self.manager.relationships if rel.identifier not in identifiers
        ]

    def update_bulk(self, updates: List[Dict[str, Any]]) -> None:
        """
        Update multiple relationships in bulk.
        Each update dict must have an 'identifier' key to find the relationship,
        along with the fields to update.
        """
        for update in updates:
            for rel in self.manager.relationships:
                if rel.identifier == update["identifier"]:
                    if "label" in update:
                        rel.label = update["label"]
                    if "description" in update:
                        rel.description = update["description"]
                    if "relation_type" in update:
                        new_relation_type = update["relation_type"]
                        # Accept either a RelationType enum or string.
                        if isinstance(new_relation_type, RelationType):
                            rel.relation_type = new_relation_type.value
                        else:
                            rel.relation_type = new_relation_type
                    # Additional updates can be handled similarly.


def build_relationship_graph(relationships: List[StandardRelationship]) -> nx.DiGraph:
    """
    Constructs a directed graph from a list of StandardRelationship instances.
    Nodes represent entity identifiers, and edges represent relationships (with attributes).
    """
    graph = nx.DiGraph()
    for rel in relationships:
        graph.add_node(rel.source.identifier)
        graph.add_node(rel.target.identifier)
        graph.add_edge(rel.source.identifier, rel.target.identifier,
                       relation_type=rel.relation_type,
                       identifier=rel.identifier,
                       sumo_class=rel.sumo_class)
    return graph


def get_centrality(graph: nx.DiGraph) -> Dict[Any, float]:
    """
    Returns the degree centrality of nodes in the graph.
    """
    return nx.degree_centrality(graph)


def find_paths(graph: nx.DiGraph, source_id: str, target_id: str) -> List[List[str]]:
    """
    Returns all simple paths between source and target entity identifiers.
    """
    try:
        return list(nx.all_simple_paths(graph, source=source_id, target=target_id))
    except nx.NetworkXNoPath:
        return []


__all__ = [
    "RelationType", "StandardRelationship",
    "RelationshipManager", "RelationshipBulkManager",
    "build_relationship_graph", "get_centrality", "find_paths"
]
