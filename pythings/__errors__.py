"""
The errors and exceptions-related code for the PyThings package.
"""


class PyThingsException(Exception):  # TODO: Finish base exception class
    """
    Base class for all **PyThings** exceptions.
    """

    def __init__(self, message: str = None):
        """
        TODO: Method docs

        :param message:
        """
        # Determine Message
        if message is None:
            self.message = 'Unknown error'
        else:
            self.message = message


class PyThingsExtensionException(PyThingsException):  # TODO: Finish exception class
    def __init__(self, message: str = None):
        """
        TODO: Method docs

        :param message:
        """
        # Determine Message
        if message is None:
            self.message = 'Unknown PyThings extension error'
        else:
            self.message = message
