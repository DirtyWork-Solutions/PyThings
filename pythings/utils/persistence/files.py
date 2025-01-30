"""
Handles local and or remote file/media storage and persistence.
"""

from abc import ABC


class BaseFileDestination(ABC):
    """
    Base for ordinary file destinations.
    """
    def __init__(self):
        pass

class LocalDestination(BaseFileDestination):
    def __init__(self):
        super().__init__()

class RemoteDestination(BaseFileDestination):
    def __init__(self):
        super().__init__()

class FileManager:  # TODO: Make a singleton
    def __init__(self):
        pass