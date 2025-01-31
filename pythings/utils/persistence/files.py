"""
Handles local and or remote file/media storage and persistence.
"""
import os
import threading
from abc import ABC, abstractmethod


class BaseFileDestination(ABC):
    """
    Base for ordinary file destinations.
    """
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def save(self, filename: str, data: bytes):
        pass

    @abstractmethod
    def load(self, filename: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, filename: str):
        pass

class LocalDestination(BaseFileDestination):
    def __init__(self):
        super().__init__()

    def save(self, filename: str, data: bytes):
        with open(os.path.join(self.path, filename), 'wb') as file:
            file.write(data)

    def load(self, filename: str) -> bytes:
        with open(os.path.join(self.path, filename), 'rb') as file:
            return file.read()

    def delete(self, filename: str):
        os.remove(os.path.join(self.path, filename))

class RemoteDestination(BaseFileDestination):
    def __init__(self):
        super().__init__()

    def save(self, filename: str, data: bytes):
        # Implement remote save logic here
        pass

    def load(self, filename: str) -> bytes:
        # Implement remote load logic here
        pass

    def delete(self, filename: str):
        # Implement remote delete logic here
        pass


class FileManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(FileManager, cls).__new__(cls)
                    cls._instance._destinations = {}
                    cls._instance._file_locks = {}
        return cls._instance

    def add_destination(self, name: str, destination: BaseFileDestination):
        with self._lock:
            self._destinations[name] = destination

    def get_destination(self, name: str) -> BaseFileDestination:
        with self._lock:
            return self._destinations.get(name)

    def _get_file_lock(self, filename: str) -> threading.Lock:
        with self._lock:
            if filename not in self._file_locks:
                self._file_locks[filename] = threading.Lock()
            return self._file_locks[filename]

    def save(self, destination_name: str, filename: str, data: bytes, use_lock: bool = True):
        destination = self.get_destination(destination_name)
        if destination:
            file_lock = self._get_file_lock(filename) if use_lock else None
            if file_lock:
                with file_lock:
                    destination.save(filename, data)
            else:
                destination.save(filename, data)

    def load(self, destination_name: str, filename: str, use_lock: bool = True) -> bytes:
        destination = self.get_destination(destination_name)
        if destination:
            file_lock = self._get_file_lock(filename) if use_lock else None
            if file_lock:
                with file_lock:
                    return destination.load(filename)
            else:
                return destination.load(filename)

    def delete(self, destination_name: str, filename: str, use_lock: bool = True):
        destination = self.get_destination(destination_name)
        if destination:
            file_lock = self._get_file_lock(filename) if use_lock else None
            if file_lock:
                with file_lock:
                    destination.delete(filename)
            else:
                destination.delete(filename)