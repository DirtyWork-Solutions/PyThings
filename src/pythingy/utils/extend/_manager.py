"""
TODO: Module docs
"""
from abc import ABC

NATIVE_EXTENSIONS = {
    "what3words": {},
    "neo4j": {}
}


class BaseExtensions(ABC):  # TODO: Implement base class
    """"""

    def activate(self):  # TODO: Implement class method
        pass

    def deactivate(self):  # TODO: Implement class method
        pass

    def validate(self):  # TODO: Implement class method
        pass


class BaseAddon(BaseExtensions, ABC):  # TODO: Implement class
    pass


class BasePlugin(BaseExtensions, ABC):  # TODO: Implement class
    pass


class BaseExpansion(BaseExtensions, ABC):  # TODO: Implement class
    pass


class Extension(BaseExtensions):  # TODO: Implement class
    pass


class ExtensionHandler:  # TODO: Make class & singleton
    pass
