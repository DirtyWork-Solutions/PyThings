from pythings.utils.extensions.what3words import words_to_coordinates, coordinates_to_words, api_key_check

class Location:
    """
    Represents a physical location.
    """

    def __init__(self, name: str, coordinates: tuple = None, what3words: tuple | str = None):
        self.name = name if name else 'unknown location'
        self.coordinates = coordinates
        self.three_words = what3words

    def get_coordinates(self, allow_inference: bool = True):
        """

        :param allow_inference: if not set, infer coordinates from what3words when present?
        :return:
        :raises ValueError:
        :raises PermissionError:

        """
        if self.coordinates:
            return self.coordinates
        elif self.coordinates is None and not allow_inference:
            raise AttributeError("Coordinates are not set.")
        elif self.three_words is not None and allow_inference:
            return words_to_coordinates(self.three_words)
        elif not self.three_words and not self.coordinates:
            raise ValueError("No coordinates available.")
        else:
            raise PermissionError("Inference is not allowed or variables not available.")

    def get_three_words(self, allow_inference: bool = False):
        """

        :param allow_inference: if not set, infer what3words from coordinates when present?
        :return:
        """
        if not api_key_check():
            raise ConnectionError("Missing API key: 'W3W_API_KEY'")
        else:
            if self.three_words:
                return self.three_words
            elif self.three_words is None and not allow_inference:
                raise AttributeError("what3words are not set.")
            elif self.three_words is not None and allow_inference:
                return coordinates_to_words(self.coordinates)
            else:
                raise PermissionError("Inference is not allowed or variables not available.")


class Geometry:
    """
    Represents a geometric shape.
    """
    def __init__(self, shape: str, dimensions: dict):
        self.shape = shape
        self.dimensions = dimensions

    def area(self) -> float:
        """
        Calculate the area of the shape.
        :return:
        :raises ValueError for unknown or unsupported shape types.
        """
        if self.shape.lower() == "circle":
            return 3.14159 * (self.dimensions.get("radius", 0) ** 2)
        else:
            raise ValueError("Unsupported shape")