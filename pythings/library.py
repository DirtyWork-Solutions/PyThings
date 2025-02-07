import logging
from abc import ABC
from typing import Any, Union
from uuid import UUID, uuid4
import cachetools

from pythings.things import Thing

class TagError(KeyError):
    """Custom exception for tag-related errors."""
    pass

class Tag:  # TODO: Make dynamic singleton
    def __init__(self, name: str, description: str | None = None):
        self.name = name
        self.description = description if description is not None else ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Tag({self.name}{f' - {self.description}' if self.description else ''})"

class TagManager:  # TODO: Make a singleton, maybe even design pattern?
    """
    Central tag manager for the library module.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TagManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._tags = {
                "active": [],
                "archived": []
            }
            self._initialized = True

    @property
    def active_tags(self):
        return self._tags["active"]

    @property
    def archived_tags(self):
        return self._tags["archived"]

    @property
    def all_tags(self):
        return self.active_tags + self.archived_tags

    def delete_tag(self, tag: str | Tag):
        """

        :param tag:
        :return:
        """
        # Tag to delete
        find_name = self._get_tag_name(tag)
        if not self._remove_tag_from_list(find_name, self.active_tags) and not self._remove_tag_from_list(find_name, self.archived_tags):
            raise TagError(f"Tag Not Found: '{find_name}' - Couldn't delete.")

        if self._remove_tag_from_list(find_name, self.active_tags):
            logging.debug(f"Tag deleted: {find_name}")
        elif self._remove_tag_from_list(find_name, self.archived_tags):
            logging.debug(f"Tag deleted: {find_name}")
        else:
            logging.info("Could not delete tag: Unknown error.")

    def _get_tag_name(self, tag: str | Tag) -> str:
        if isinstance(tag, str):
            return tag
        elif isinstance(tag, Tag):
            return tag.name
        else:
            raise TagError("Tag Not Found. Couldn't delete.")

    def _remove_tag_from_list(self, tag_name: str, tag_list: list) -> bool:
        for t in tag_list:
            if tag_name == t.name:
                tag_list.remove(t)
                return True
        return False


    def create_tag(self, name: str, description: str | None) -> None:
        if any(t.name == name for t in self._tags["active"]) or any(t.name == name for t in self._tags["archived"]):
            logging.error(f"Tag Exists: '{name}' - Couldn't create library tag.")
        else:
            self._tags["active"].append(Tag(name, description if description else ''))

    def archive_tag(self, tag: str | Tag):
        if isinstance(tag, str):
            find_name = tag
        elif isinstance(tag, Tag):
            find_name = tag.name
        else:
            raise KeyError("Tag Not Found. Couldn't archive.")
        for t in self.active_tags:
            if find_name == t.name:
                self.active_tags.remove(t)
                self.archived_tags.append(t)
                logging.info(f"Tag archived: {t}")
                return
        raise KeyError("Tag Not Found. Couldn't archive.")

class ShelfEntry:
    def __init__(self, thing: Thing):
        self._thing = thing

    def __str__(self):
        return str(self._thing)

    def __getattr__(self, item):
        return getattr(self._thing, item)

    def __setattr__(self, key, value):
        setattr(self._thing, key, value)

    def __delattr__(self, item):
        delattr(self._thing, item)


class LibraryShelf:
    _instances = {}

    def __new__(cls, name, *args, **kwargs):
        if name not in cls._instances:
            cls._instances[name] = super(LibraryShelf, cls).__new__(cls)
        return cls._instances[name]

    def __init__(self, name: str, initial_entries: list | set | None = None):
        if not hasattr(self, '_initialized'):
            self.name = name if name else 'Unknown'
            self._entries = set(initial_entries) if initial_entries else set()
            self._initialized = True

    def check_shelf(self, search: str | Thing, fuzzy: bool = False) -> list | Thing:
        results = []
        for entry in self._entries:
            if isinstance(search, str):
                if fuzzy:
                    if search.lower() in entry.name.lower():
                        results.append(entry)
                else:
                    if search == entry.name:
                        return entry
            elif isinstance(search, Thing):
                if search == entry:
                    return entry
        return results if results else None

    def add_to_shelf(self, entry: ShelfEntry):
        self._entries.add(entry)

    def get_shelf(self):
        return self._entries

class BaseLibrary(ABC):
    def __init__(self, name: str):
        self._shelves = []  # TODO: Change to set?
        self.name = name if name is not None else 'Unknown Library'

    def add_shelf(self, shelf: LibraryShelf):  # TODO: Create method
        """
        Add a shelf to the library.

        :param shelf: (*LibraryShelf*) the shelf to add.
        :return: nothing

        :raises KeyError: if the shelf is already in the library.
        """
        if shelf in self._shelves:
            raise KeyError("Shelf already exists in the library.")
        self._shelves.add(shelf)

class ThingLibrary(BaseLibrary):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThingLibrary, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__(name='Things')
            self._initialized = True


if __name__ == '__main__':
    lib = TagManager()
    lib.create_tag('test', 'this is a test tag')
    lib.create_tag('test2', 'this is a test tag')
    print(lib.active_tags)
    lib.archive_tag('test2')
    lib.create_tag('test3', 'this is another test tag')
    print(lib.active_tags)
    library = ThingLibrary()