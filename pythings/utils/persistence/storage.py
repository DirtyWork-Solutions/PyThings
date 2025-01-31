from pythings.utils.persistence.files import FileManager
from pythings.utils.persistence.object import ObjectManager
from pythings.utils.persistence.records import DatabaseManager


class StorageLocations:  # TODO: Make a singleton
    """
    Globally holds storage destinations.
    """
    def __init__(self):
        self._file_locations = FileManager()
        self._object_locations = ObjectManager()
        self._database_locations = DatabaseManager()


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
        return self._database_locations

    def get_destination(self, destination_name: str):
        """
        Get a specific destination.
        :param destination_name:
        :return:
        """
        pass
