"""
TODO: root module docs
"""

from abc import abstractmethod, ABC

from pythings.commons.entity.abstract import BaseAbstractEntity


class BaseEntity(ABC):  # TODO: Implement base class
    """
    TODO: Class docs
    """

    @abstractmethod
    def __init__(self):
        """
        TODO: Method docs
        """

        pass

    def __repr__(self):
        return f"Entity()"


class BaseAttribute(BaseAbstractEntity, ABC):  # TODO: Implement base class
    """
    TODO: Class docs
    """

    @abstractmethod
    def __init__(self):
        """
        TODO: Method docs
        """
        super().__init__()


class BaseMeta(ABC):  # TODO: Implement base class
    """
    TODO: Class docs
    """

    @abstractmethod
    def __init__(self):
        """
        TODO: Method docs
        """

    def get_all_meta(self, as_dict: bool = True):  # TODO: Implement method
        """
        TODO: method docs

        :param as_dict:
        :return:
        """
        pass

    def get_meta(self, category_name: str):  # TODO: Implement method
        """
        Get a whole meta category/group

        :param category_name:
        :return:
        """
        pass

    def get_metakey(self, key_name: str, category: str = None, soft_fail: bool = False):  # TODO: Implement method
        """
        Get a single meta-value from the keyname. *Optionally specific the category/group, otherwise return first result
        if any.*

        :param key_name: (str) | name of the dict key.
        :param category: (str) | category/group to filter in search, if any.
        :param soft_fail: (bool) | return None in case of error/lack of result? *Default is raise error*.
        :return: (Dict)
        :raises KeyError: (Key Not Found) | if key doesn't exist.
        :raises ValueError: (Category Not Found) | if the category/group dict is not found.
        """
        pass