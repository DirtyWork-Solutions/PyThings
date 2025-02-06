"""
TODO: module docs
"""
from abc import ABC, abstractmethod

from pythings.__base__ import BaseEntity, Entity, BaseAttribute, BaseAbstractEntity, BasePhysicalEntity, \
    BaseRelationship


class PhysicalEntity(BasePhysicalEntity):  # TODO: implement class
    """
    TODO: class docs
    """

    def __init__(self, name: str = 'unknown entity'):
        """
        TODO: method docs

        :param name:
        """
        self.name = name


class Object(PhysicalEntity):
    """
    TODO: class docs
    """

    def __init__(self, name: str = 'unknown object', material: str = 'unknown material'):
        """
        TODO: method docs

        :param name:
        :param material:
        """
        super().__init__(name)
        self.material = material
