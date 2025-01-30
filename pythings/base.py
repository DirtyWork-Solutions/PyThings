from abc import ABC, abstractmethod


class BaseThing(ABC):
    """
    Base class for all **Things**.

    A *Thing* is a generic abstraction for anything, composable by default.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialise an instance of a **Thing**.
        """
        pass

class Thing(BaseThing):
    """
    A generic abstraction for anything, composable by default.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialise an instance of a **Thing**.
        """
        super().__init__()

class FoundationalThing(Thing):
    """
    A foundational **Thing**.  # TODO: Improve these docs
    """


    def __init__(self):
        super().__init__()

class Attribute(BaseThing):
    """
    A generic abstraction for an *attribute* of a **Thing**.
    """


    def __init__(self):
        super().__init__()

class Metadata(BaseThing):
    """
    A generic abstraction for *metadata* of a **Thing**.
    """


    def __init__(self):
        super().__init__()

class BaseRelationship(BaseThing):
    """
    Base class for all **relationship** classes.
    """

    @abstractmethod
    def __init__(self):
        super().__init__()

class Relationship(BaseRelationship):
    """
    Represents a *relationship* between **Things**.
    """


    def __init__(self):
        super().__init__()
