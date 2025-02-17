"""
TODO: module docs
"""

from src.pythingd.__base__ import BasePhysicalEntity


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
