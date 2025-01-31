import unittest
from uuid import UUID
from pythings.base import BaseThing, Thing, FoundationalThing, Attribute, Metadata, BaseRelationship, Relationship, BaseInterface, Interface

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

if __name__ == '__main__':
    unittest.main()

class TestBaseThing(unittest.TestCase):
    def test_base_thing(self):
        with self.assertRaises(TypeError):
            BaseThing()

class TestThing(unittest.TestCase):
    def test_thing_initialization(self):
        thing = Thing()
        self.assertIsInstance(thing._metadict, Metadata)

class TestFoundationalThing(unittest.TestCase):
    def test_foundational_thing_initialization(self):
        foundational_thing = FoundationalThing()
        self.assertIsInstance(foundational_thing, FoundationalThing)

class TestAttribute(unittest.TestCase):
    def test_attribute_initialization(self):
        attribute = Attribute(name="color", value="blue", description="The color of the thing")
        self.assertEqual(attribute.name, "color")
        self.assertEqual(attribute.value, "blue")
        self.assertEqual(attribute.description, "The color of the thing")

class TestMetadata(unittest.TestCase):
    def test_metadata_initialization(self):
        metadata = Metadata()
        self.assertIsInstance(metadata._metadict["uid"], UUID)

    def test_metadata_getattr(self):
        metadata = Metadata()
        metadata._metadict["test"] = {"key": "value"}
        self.assertEqual(metadata.__getattr__("test.key"), "value")

    def test_metadata_repr(self):
        metadata = Metadata()
        self.assertTrue(repr(metadata).startswith("Metadata"))

    def test_metadata_mappings(self):
        metadata = Metadata()
        self.assertIsInstance(metadata.mappings, dict)

class TestBaseRelationship(unittest.TestCase):
    def test_base_relationship(self):
        with self.assertRaises(TypeError):
            BaseRelationship()

class TestRelationship(unittest.TestCase):
    def test_relationship_initialization(self):
        relationship = Relationship()
        self.assertIsInstance(relationship.metadata, Metadata)

class TestBaseInterface(unittest.TestCase):
    def test_base_interface(self):
        with self.assertRaises(TypeError):
            BaseInterface()

class TestInterface(unittest.TestCase):
    def test_interface_initialization(self):
        interface = Interface()
        self.assertIsInstance(interface, Interface)

if __name__ == '__main__':
    unittest.main()