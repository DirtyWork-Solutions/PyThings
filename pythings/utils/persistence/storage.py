import threading
from pythings.utils.persistence.files import FileManager
from pythings.utils.persistence.object import ObjectManager
from pythings.utils.persistence.records import DatabaseManager

class StorageLocations:
    """
    Globally holds storage destinations.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(StorageLocations, cls).__new__(cls)
                    cls._instance._file_locations = FileManager()
                    cls._instance._object_locations = ObjectManager()
                    cls._instance._database_locations = DatabaseManager()
        return cls._instance

    @property
    def files(self):
        """
        Get all file destinations.
        :return:
        """
        return self._file_locations

    @property
    def objects(self):
        """
        Get all object destinations.
        :return:
        """
        return self._object_locations

    @property
    def databases(self):
        """
        Get all database destinations.
        :return:
        """
        return self._database_locations

    def get_destination(self, destination_name: str):
        """
        Get a specific destination.
        :param destination_name:
        :return:
        """
        if destination_name in self._file_locations._destinations:
            return self._file_locations.get_destination(destination_name)
        elif destination_name in self._object_locations._destinations:
            return self._object_locations.get_destination(destination_name)
        elif destination_name in self._database_locations._destinations:
            return self._database_locations.get_destination(destination_name)
        else:
            return None