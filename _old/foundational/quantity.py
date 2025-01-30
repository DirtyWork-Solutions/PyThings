from pint import UnitRegistry

ureg = UnitRegistry()

class Quantity:
    """
    Represents a measurable quantity (*using **Pint** if possible*).
    """
    def __init__(self, value, unit):
        """
        Initialize a Quantity.
        :param value: (float) Numeric value of the quantity.
        :param unit: (str) Unit as a string (e.g. "kg", "m", "second")
        """
        self.value = value
        self.unit = unit

    def to(self, target_unit):
        """
        Convert the quantity to another unit.
        :param target_unit:
        :return:
        """
        try:
            converted_value = self.value.to(target_unit)
            return  Quantity(converted_value.magnitude, converted_value.units)
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