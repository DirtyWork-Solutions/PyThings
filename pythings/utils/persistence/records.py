"""
Handles database, and relational record keeping.
"""
# pythings/utils/persistence/records.py

import threading
import sqlite3
import psycopg2  # TODO: Make optional?
import mysql.connector  # TODO: Make optional?
from abc import ABC, abstractmethod

class BaseDatabaseDestination(ABC):
    """
    Base class for database destinations.
    """
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, query: str, params: tuple = ()):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def batch_query(self, queries: list):
        pass

class SQLiteDestination(BaseDatabaseDestination):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.connection_string)

    def query(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def batch_query(self, queries: list):
        cursor = self.connection.cursor()
        try:
            for query, params in queries:
                cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

class PostgreSQLDestination(BaseDatabaseDestination):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(self.connection_string)

    def query(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def batch_query(self, queries: list):
        cursor = self.connection.cursor()
        try:
            for query, params in queries:
                cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

class MySQLDestination(BaseDatabaseDestination):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(self.connection_string)

    def query(self, query: str, params: tuple = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def batch_query(self, queries: list):
        cursor = self.connection.cursor()
        try:
            for query, params in queries:
                cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._destinations = {}
        return cls._instance

    def add_destination(self, name: str, destination: BaseDatabaseDestination):
        with self._lock:
            self._destinations[name] = destination

    def get_destination(self, name: str) -> BaseDatabaseDestination:
        with self._lock:
            return self._destinations.get(name)

    def query(self, destination_name: str, query: str, params: tuple = ()):
        destination = self.get_destination(destination_name)
        if destination:
            return destination.query(query, params)
        return None

    def batch_query(self, destination_name: str, queries: list):
        destination = self.get_destination(destination_name)
        if destination:
            return destination.batch_query(queries)
        return None

    def close(self, destination_name: str):
        destination = self.get_destination(destination_name)
        if destination:
            destination.close()