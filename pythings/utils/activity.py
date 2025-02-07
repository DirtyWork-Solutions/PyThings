from abc import ABC, abstractmethod

from pythings.base import Metadata


class BaseHook(ABC):
    """

    """
    @abstractmethod
    def __init__(self, name: str, priority: int):
        """

        :param name:
        :param priority:
        """
        self.name: name
        self.priority: priority  # TODO: Introduce priorities  to hooks.
        self._metadict = Metadata()
    @property
    def metadata(self):
        return self._metadict

    @abstractmethod
    def execute(self, thing):
        """

        :param thing:
        :return:
        """
        pass

class Hook(BaseHook):
    """

    """
    def __init__(self, name: str = 'unknown hook'):
        """

        :param name:
        """
        self.name = name
        self._metadict = Metadata()

    def execute(self, thing):  # TODO: Add more parameters and default behaviour
        """

        :param thing:
        :return:
        """
        pass

#
class ActivityHookManager:  # TODO: Make singleton

    def __init__(self):
        self._hooks = {}

    def register_hook(self, name: str, hook: BaseHook):
        if name not in self._hooks:
            self._hooks[name] = []
        self._hooks[name].append(hook)

    def unregister_hook(self, name: str, hook: BaseHook):
        if name in self._hooks:
            self._hooks[name].remove(hook)
            if not self._hooks[name]:
                del self._hooks[name]

    def execute_hooks(self, name: str, *args, **kwargs):
        if name in self._hooks:
            for hook in self._hooks[name]:
                hook.execute(*args, **kwargs)