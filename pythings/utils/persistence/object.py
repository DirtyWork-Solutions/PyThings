"""
Handles object storage.
"""

import threading
import pickle
from abc import ABC, abstractmethod

class BaseObjectDestination(ABC):
    """
    Base class for object destinations.
    """
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def save(self, object_name: str, obj: object):
        pass

    @abstractmethod
    def load(self, object_name: str) -> object:
        pass

    @abstractmethod
    def delete(self, object_name: str):
        pass

class LocalObjectDestination(BaseObjectDestination):
    def __init__(self, path: str):
        super().__init__(path)

    def save(self, object_name: str, obj: object):
        with open(f"{self.path}/{object_name}.pkl", 'wb') as file:
            pickle.dump(obj, file)

    def load(self, object_name: str) -> object:
        with open(f"{self.path}/{object_name}.pkl", 'rb') as file:
            return pickle.load(file)

    def delete(self, object_name: str):
        os.remove(f"{self.path}/{object_name}.pkl")

class ObjectManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ObjectManager, cls).__new__(cls)
                    cls._instance._destinations = {}
        return cls._instance

    def add_destination(self, name: str, destination: BaseObjectDestination):
        with self._lock:
            self._destinations[name] = destination

    def get_destination(self, name: str) -> BaseObjectDestination:
        with self._lock:
            return self._destinations.get(name)

    def save(self, destination_name: str, object_name: str, obj: object):
        destination = self.get_destination(destination_name)
        if destination:
            destination.save(object_name, obj)

    def load(self, destination_name: str, object_name: str) -> object:
        destination = self.get_destination(destination_name)
        if destination:
            return destination.load(object_name)
        return None

    def delete(self, destination_name: str, object_name: str):
        destination = self.get_destination(destination_name)
        if destination:
            destination.delete(object_name)