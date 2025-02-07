import unittest

from pythings.base import Thing, Metadata, BaseThing


class TestThing(unittest.TestCase):

    def test_thing_serialization(self):
        thing = Thing()
        thing_json = thing.to_json()
        deserialized_thing = Thing.from_json(thing_json)
        self.assertEqual(thing, deserialized_thing)

    def test_thing_equality(self):
        thing1 = Thing()
        thing2 = Thing()
        self.assertNotEqual(thing1, thing2)
        thing2._metadict = thing1._metadict
        self.assertEqual(thing1, thing2)

    def test_thing_hashing(self):
        thing = Thing()
        thing_set = {thing}
        self.assertIn(thing, thing_set)


class TestMetadata(unittest.TestCase):

    def test_metadata_serialization(self):
        metadata = Metadata()
        metadata_json = metadata.to_json()
        deserialized_metadata = Metadata.from_json(metadata_json)
        self.assertEqual(metadata, deserialized_metadata)

    def test_metadata_equality(self):
        metadata1 = Metadata()
        metadata2 = Metadata()
        self.assertNotEqual(metadata1, metadata2)
        metadata2._metadict = metadata1._metadict
        self.assertEqual(metadata1, metadata2)

    def test_metadata_hashing(self):
        metadata = Metadata()
        metadata_set = {metadata}
        self.assertIn(metadata, metadata_set)


class TestBaseThing(unittest.TestCase):
    def test_base_thing(self):
        with self.assertRaises(TypeError):
            BaseThing()
