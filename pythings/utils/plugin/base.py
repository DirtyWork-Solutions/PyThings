from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """
    Additional code that extends, enhances, or SOMETHING the package.
    """
    """
        Base class for all plugins.

        Plugins are additional code that extends or enhances the package.
        """

    @abstractmethod
    def activate(self):
        """
        Activate the plugin.
        """
        pass

    @abstractmethod
    def deactivate(self):
        """
        Deactivate the plugin.
        """
        pass

class Plugin(BasePlugin):
    """
        A concrete implementation of a plugin.
        """

    def activate(self):
        """
        Activate the plugin.
        """
        print("Plugin activated")

    def deactivate(self):
        """
        Deactivate the plugin.
        """
        print("Plugin deactivated")

class BaseExtension(BasePlugin, ABC):
    """
    A plugin (part of) that extends the features, and  or, functionality of the package.
    """
    """
        Base class for extensions.

        Extensions are plugins that extend the features or functionality of the package.
        """

    @abstractmethod
    def activate(self):
        """
        Extend the functionality.
        """
        pass

    @abstractmethod
    def deactivate(self):
        """
        Remove the extension.
        """

        pass

class Extension(BaseExtension):
    """
        A concrete implementation of an extension.
        """

    def activate(self):
        """
        Activate the extension.
        """
        print("Extension activated")

    def deactivate(self):
        """
        Deactivate the extension.
        """
        print("Extension deactivated")

class BaseDomain(BaseExtension, ABC):
    """
    Plugins that introduce focused and niched ontology domains.
    """
    """
        Base class for domain-specific plugins.

        Domains introduce focused and niched ontology domains.
        """

    @abstractmethod
    def define_domain(self):
        """
        Define the domain.
        """
        pass

class Domain(BaseDomain):
    """
    An ontology domain.
    """
    """
        A concrete implementation of a domain.
        """

    def activate(self):
        """
        Activate the domain.
        """
        print("Domain activated")

    def deactivate(self):
        """
        Deactivate the domain.
        """
        print("Domain deactivated")

    def define_domain(self):
        """
        Define the domain.
        """
        print("Domain defined")
