from entity.bases import BaseEntity


class PhysicalEntity(BaseEntity):
    def __init__(self, name: str = 'unknown entity'):
        self.name = name

class Object(PhysicalEntity):
    def __init__(self, name: str = 'unknown object', material: str = 'unknown material'):
        super().__init__(name)
        self.material = material