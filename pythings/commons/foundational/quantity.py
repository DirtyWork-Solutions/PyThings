"""
TODO: Module docs for Quantity
"""
from typing import Optional
from uuid import UUID, uuid4

from pint import UnitRegistry, Unit

from pythings.__base__ import BaseEntity, Entity, BaseAttribute, BaseAbstractEntity, BasePhysicalEntity, \
    BaseRelationship

# Initialize the Pint unit registry.
ureg = UnitRegistry()


class Quantity(BaseAbstractEntity):
    """
    A base class representing any measurable quantity.

    *Uses Pint internally to manage numerical values and units.*
    """

    def __init__(self, value: float | int,
                 unit: str | Unit,
                 label: Optional[str] = 'quantity',
                 entity_id: str | UUID = uuid4()):
        """
        Initializes a Quantity.

        Parameters:
        - value: The numerical magnitude.
        - unit: A string or Pint unit defining the measurement unit.
        """
        super().__init__(identifier=entity_id, label=label, description=f"{value} {unit}")
        self._quantity = value * ureg(unit)

    @property
    def magnitude(self):
        """Returns the numerical value (magnitude) of the quantity."""
        return self._quantity.magnitude

    @property
    def unit(self):
        """Returns the unit of the quantity."""
        return self._quantity.units

    def to(self, new_unit):
        """
        Converts the quantity to a new unit.

        Parameters:
        - new_unit: The unit to convert to (as a string or Pint unit).

        Returns:
        A new Quantity instance in the requested unit.
        """
        converted = self._quantity.to(new_unit)
        return Quantity(converted.magnitude, str(converted.units))

    def __add__(self, other):
        """
        Adds two quantities if they are compatible.

        Raises a TypeError if the other operand is not a Quantity.
        """
        if isinstance(other, Quantity):
            result = self._quantity + other._quantity
            return Quantity(result.magnitude, str(result.units))
        return NotImplemented

    def __sub__(self, other):
        """
        Subtracts one quantity from another if they are compatible.

        Raises a TypeError if the other operand is not a Quantity.
        """
        if isinstance(other, Quantity):
            result = self._quantity - other._quantity
            return Quantity(result.magnitude, str(result.units))
        return NotImplemented

    def __mul__(self, other):
        """
        Multiplies the quantity either by a scalar (int or float)
        or by another Quantity.
        """
        if isinstance(other, (int, float)):
            result = self._quantity * other
            return Quantity(result.magnitude, str(result.units))
        elif isinstance(other, Quantity):
            result = self._quantity * other._quantity
            return Quantity(result.magnitude, str(result.units))
        return NotImplemented

    def __truediv__(self, other):
        """
        Divides the quantity either by a scalar (int or float)
        or by another Quantity.
        """
        if isinstance(other, (int, float)):
            result = self._quantity / other
            return Quantity(result.magnitude, str(result.units))
        elif isinstance(other, Quantity):
            result = self._quantity / other._quantity
            return Quantity(result.magnitude, str(result.units))
        return NotImplemented

    def __repr__(self):
        return f"Quantity({self._quantity.magnitude}, '{self._quantity.units}')"


# Example usage:
if __name__ == '__main__':
    # Create two lengths measured in meters.
    length1 = Quantity(5, 'meter')
    length2 = Quantity(3, 'meter')

    # Add the two lengths.
    total_length = length1 + length2
    print("Total Length:", total_length)  # Expected: Quantity(8, 'meter')

    # Convert the total length to feet.
    total_length_in_feet = total_length.to('foot')
    print("Total Length in Feet:", total_length_in_feet)

    # Multiply to get an area (meter * meter = square meter).
    area = length1 * length2
    print("Area:", area)

    print(length1.label)
