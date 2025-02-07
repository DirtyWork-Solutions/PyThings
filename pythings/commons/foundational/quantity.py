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
    Uses Pint internally to manage numerical values and units.
    """

    def __init__(self, value, unit,
                 identifier: str | UUID = uuid4()):
        """
        Initializes a Quantity.

        Parameters:
          - value: The numerical magnitude.
          - unit: A string or Pint unit defining the measurement unit.
        """
        super().__init__(identifier=identifier, label=str(unit) + " quantity", description="A quantity with a unit.",
                         sumo_class="Quantity")  # TODO: Check inputs and SUMO class
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
        """Adds two quantities if they are compatible."""
        if isinstance(other, Quantity):
            result = self._quantity + other._quantity
            return Quantity(result.magnitude, str(result.units))
        return NotImplemented

    def __sub__(self, other):
        """Subtracts one quantity from another if they are compatible."""
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


class DerivedQuantity(Quantity):
    """
    A subclass of Quantity that provides a human-friendly label for derived units.

    Derived units (*e.g., area, velocity, acceleration*) arise from arithmetic
    on base quantities. This class inspects the dimensionality (*via Pint*) and
    maps it to a known friendly name.
    """
    # Map from a frozenset of (dimension, exponent) pairs to a derived unit name.
    # For example, velocity in Pint has dimensionality {'[length]': 1, '[time]': -1}.
    DERIVED_UNIT_NAMES = {
        frozenset({('length', 1)}): "length",
        frozenset({('length', 1), ('time', -1)}): "velocity",
        frozenset({('length', 1), ('time', -2)}): "acceleration",
        frozenset({('length', 2)}): "area",
        frozenset({('length', 3)}): "volume",
        # Additional mappings can be added here as needed.
    }

    def __init__(self, value, unit):
        super().__init__(value, unit)

    def get_derived_unit_name(self):
        """
        Inspects the quantity's dimensionality and returns a friendly derived unit name.
        If the dimensionality is not recognized, returns a string representation of it.
        :return: A human-friendly name for the derived unit **or** a string representation.
        """
        # Get the dimensionality from the internal Pint quantity.
        # Pint returns a dict like {'[length]': 1, '[time]': -1} for velocity.
        dim = self._quantity.dimensionality

        # Normalize by stripping the square brackets from the keys.
        normalized = {key.strip('[]'): power for key, power in dim.items()}

        # Convert the normalized dict to a frozenset of (dimension, exponent) pairs.
        key_frozen = frozenset(normalized.items())

        # Look up the friendly name.
        return self.DERIVED_UNIT_NAMES.get(key_frozen, str(normalized))


# Example usage:
if __name__ == '__main__':
    # Creating base quantities.
    length = DerivedQuantity(5, 'meter')
    time_interval = DerivedQuantity(2, 'second')

    # Derived quantity: Velocity (meter/second) is created by dividing length by time.
    velocity = length / time_interval
    print("Velocity:", velocity)  # Expected: Quantity(2.5, 'meter/second')

    # Display the friendly derived unit name.
    # Velocity's dimensionality is {'[length]': 1, '[time]': -1} which we map to "velocity".
    # The get_derived_unit_name method should output "velocity".
    print("Derived unit name for velocity:",
          DerivedQuantity(velocity.magnitude, str(velocity.unit)).get_derived_unit_name())

    # Another derived example: Area (meter^2)
    width = DerivedQuantity(3, 'meter')
    area = length * width
    print("Area:", area)  # Expected: Quantity(15, 'meter**2')
    print("Derived unit name for area:",
          DerivedQuantity(area.magnitude, str(area.unit)).get_derived_unit_name())
