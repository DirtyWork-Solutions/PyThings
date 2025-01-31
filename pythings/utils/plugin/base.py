from abc import ABC


class BasePlugin(ABC):
    """
    Additional code that extends, enhances, or SOMETHING the package.
    """
    pass

class Plugin(BasePlugin):
    pass

class BaseExtension(BasePlugin, ABC):
    """
    A plugin (part of) that extends the features, and  or, functionality of the package.
    """
    pass

class Extension(BaseExtension):
    pass

class BaseDomain(BaseExtension, ABC):
    """
    Plugins that introduce focused and niched domains.
    """
    pass

class Domain(BaseDomain):
    pass

