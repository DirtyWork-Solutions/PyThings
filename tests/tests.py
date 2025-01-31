import unittest
from pythings.library import TagManager, Tag, LibraryShelf, ThingLibrary
import unittest
from pythings.library import TagManager, Tag

class TestTagManager(unittest.TestCase):
    def setUp(self):
        self.tag_manager = TagManager()

    def test_create_tag(self):
        self.tag_manager.create_tag('test', 'this is a test tag')
        self.assertEqual(len(self.tag_manager.active_tags), 1)
        self.assertEqual(self.tag_manager.active_tags[0].name, 'test')

    def test_archive_tag(self):
        self.tag_manager.create_tag('test', 'this is a test tag')
        self.tag_manager.archive_tag('test')
        self.assertEqual(len(self.tag_manager.archived_tags), 1)
        self.assertEqual(self.tag_manager.archived_tags[0].name, 'test')

    def test_delete_tag(self):
        self.tag_manager.create_tag('test', 'this is a test tag')
        self.tag_manager.delete_tag('test')
        self.assertEqual(len(self.tag_manager.active_tags), 0)

if __name__ == '__main__':
    unittest.main()