from pythings.base import Thing, Metadata, Attribute


class BaseEntity(Thing):
    """
    Base class for all entity classes.
    """
    def __init__(self, name: str, description: str = None):
        super().__init__()
        self.name = name
        self.description = description if description else 'No description available.'

    def __repr__(self):
        return f"Entity(name={self.name}')"



class Entity(BaseEntity):
    """
    Represents an entity.
    """
    def __init__(self, name: str, description: str = None):
        super().__init__(name, description)
        self.metadata = Metadata()
        self.attributes = []

    def add_attribute(self, attribute: Attribute | dict):
        """
        Add an attribute to the entity.
        :param attribute: the attribute to add.
        :return: nothing
        """
        self.attributes.append(attribute)

    def remove_attribute(self, attribute: Attribute | str):
        """
        Remove an attribute from the entity.
        :param attribute: the attribute to remove.
        :return: nothing
        """
        self.attributes.remove(attribute)

    def update_attribute(self, attribute: Attribute | str):
        """
        Update an attribute.
        :param attribute: the attribute to update.
        :return: nothing
        """
        self.attributes.remove(attribute)
        self.attributes.append(attribute)



class PhysicalThing(Entity):
    """
    Represents entities that exist in time and space.
    """
    def __init__(self, name: str, description: str = None,
                 is_process: bool = False):
        super().__init__(name, description)
        self.is_process = is_process

    def __repr__(self):
        return f"PhysicalThing(name={self.name}, description={self.description})"



class AbstractThing(Entity):
    """
    Represents an abstract thing that does not have a physical presence.
    """
    def __init__(self, name: str, description: str = None, category: str = None):
        """

        :param name:
        :param description: Optional - a description of the thing.
        :param category: The type of abstract entity (e.g. 'concept', 'quantity', 'relation').
        """
        super().__init__(name, description)
        self.category = category if category else 'unknown'


    def __repr__(self):
        return f"AbstractThing(name={self.name}, category={self.category})"

if __name__ == '__main__':
    test = AbstractThing('democracy', 'a form of government', 'concept')
    device = PhysicalThing('hammer', 'a tool for hitting nails')
    print(test)
    print(device)