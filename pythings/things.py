"""
Quick Imports & Interfaces
"""

import logging
logging.basicConfig(level=logging.DEBUG)
from pythings.base import Metadata



class Thing:
    """
    A **Thing** is a generic entity that can be used to represent any object or concept.
    """
    def __init__(self, ):
        """
        Initialise an instance of a **Thing**.
        """
        self._settings = {}
        self._metadata = Metadata()
        self._attributes = {}
        logging.debug(f"Thing initialised: {self.uid}")

    def __str__(self):
        return f"{self.__class__.__name__}: {self.uid}"

    def __repr__(self):
        return f"{self.__class__.__name__}(uid={self.uid})"
    @property
    def uid(self):
        return self._metadata.uid

    @property
    def metadata(self):
        return self._metadata

class ThingBuilder:  # TODO: Add methods
    """
    A **ThingBuilder** is a class that is used to build instances of a **Thing**.
    """

    def __init__(self):
        self._thing = None

    def build(self, return_thing: bool = False):
        """
        Build an instance of a **Thing** with the given configuration.

        :param return_thing: (*bool*) also return the built instance? Default is **False**.
        :return: Thing (*Conditional*) the instance. If **return_thing** is **True**.
        :raises Exception: if the **Thing** could not be built.
        """

        #
        try:
            logging.debug(f"Building thing...")
            self._thing = Thing()
        except Exception as e:
            logging.error("Could not build thing.")
            raise e

        #
        logging.info(f"Thing built: {self._thing}{'' if not return_thing else ' (returned)'}")
        if return_thing:
            return self._thing

class ThingManager:
    """
    A **ThingManager** is a class that is used to manage instances of a **Thing**.
    """
    pass


def load_thing():  # TODO: Implement
    """

    :return:
    """
    loaded = None

    logging.warning("Thing loader not implemented.")
    return Thing()

class TestThing(Thing):

    def __init__(self):
        super().__init__()

if __name__ == '__main__':

    something = Thing()
    another_thing = TestThing()
    builder = ThingBuilder()
    builder.build(return_thing=True)
    print(something.uid)
    print(something)
    print(str(another_thing))

