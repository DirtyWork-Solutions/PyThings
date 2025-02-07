"""
TODO: module docs
"""

from abc import ABC, abstractmethod
from typing import List, AnyStr
from pythings.__errors__ import PyThingsException


class BaseMixin(ABC):  # TODO: Make a part of PyExpand
    """
    Base class for Mixins.
    """

    @abstractmethod
    def __init__(self):
        """
        TODO: method docs
        """
        pass
