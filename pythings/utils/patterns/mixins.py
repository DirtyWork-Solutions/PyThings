"""
TODO: module docs
"""

from abc import ABC, abstractmethod
from typing import List, AnyStr
from pythings.__base__ import BaseMeta
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


class Metadata(BaseMeta):  # TODO: Move?
    """
    TODO: class docs
    """

    def __init__(self):
        """

        """
        super().__init__()


class MetadataMixin(BaseMixin):  # TODO: Implement class
    """
    TODO: Class docs
    """

    # Default meta-dict schemas
    _schemas = {
        "def_meta": {
        },
        "def_mappings": {

        }
    }

    def __init__(self, apply_schemas: str | List[AnyStr] = None):
        """
        TODO: method docs

        :param apply_schemas:
        """
        super().__init__()
        self._meta = Metadata()

        #
        if apply_schemas:
            pass
        else:
            pass


class MappingsMixin(BaseMixin, MetadataMixin):  # TODO: Implement class
    """
    TODO: class docs
    """

    def __init__(self):
        """
        TODO: method docs
        """
        super().__init__()
