from pint import UnitRegistry

from pythings.base import FoundationalThing

unit_registry = UnitRegistry()

class Quantity(FoundationalThing):
    """
    Represents a measurable quantity (*using **Pint** if possible*).
    """
    def __init__(self, value: float | int, unit):
        """
        Initialize a Quantity.
        :param value: (float) Numeric value of the quantity.
        :param unit: (str) Unit as a string (e.g. "kg", "m", "second")
        """
        super().__init__()
        self.value = value
        self.unit = unit

    def to(self, target_unit):  # TODO: create method
        """
        Convert the quantity to another unit.
        :param target_unit: name of the unit *(e.g. cm)*.
        :return: (*float*) converted quantity
        :raises ValueError:
        """
        try:
            converted_value = self.value.to(target_unit)
            return Quantity(converted_value.magnitude, converted_value.units)
        except Exception as e:
            raise ValueError(f"Conversion to {target_unit} failed: {e}")


    def __add__(self, other):
            """
            Add two quantities with compatible units.
            :param other:
            :return:
            """
            if not isinstance(other, Quantity):
                raise TypeError("Can only add quantity instances.")
            else:
                return Quantity((self.value + other.value).magnitude, str(self.value.units))

    def __sub__(self, other):
        """
        Subtract two quantities with compatible units.
        :param other:
        :return:
        """
        if not isinstance(other, Quantity):
            raise TypeError("Can only subtract quantity instances.")
        else:
            return Quantity((self.value - other.value).magnitude, str(self.value.units))

    def __mul__(self, other):
        """
        Multiply two quantities.
        :param other:
        :return:
        """
        if not isinstance(other, Quantity):
            raise TypeError("Can only multiply quantity instances.")
        else:
            return Quantity((self.value * other.value).magnitude, str(self.value.units))

    def __truediv__(self, other):
        """
        Divide two quantities.
        :param other:
        :return:
        """
        if not isinstance(other, Quantity):
            raise TypeError("Can only divide quantity instances.")
        else:
            return Quantity((self.value / other.value).magnitude, str(self.value.units))