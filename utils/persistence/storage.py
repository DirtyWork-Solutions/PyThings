from utils.persistence.files import FileManager, LocalDestination, RemoteDestination, BaseFileDestination
from utils.persistence.object import ObjectManager, ObjectDestination
from utils.persistence.records import DatabaseManager, BaseDatabaseDestination



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
        return self._file_locations

    @property
    def objects(self):
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
