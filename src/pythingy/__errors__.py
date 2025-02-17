"""
Module for defining and handling errors in PyThings.
"""

from datetime import datetime
import logging

# Variable holding the error codes and their descriptions.
ERROR_CODES = {
    0: "An unknown error occurred in PyThings.",
    100: "Validation error occurred.",
    101: "Configuration error occurred.",
    102: "Connection error occurred.",
    103: "Timeout error occurred.",
    104: "Permission error occurred.",
    200: "File not found.",
    201: "File read error.",
    202: "File write error.",
    300: "Database connection error.",
    301: "Database query error.",
    400: "API request error.",
    401: "API response error."
}

def validate_error_code(code_to_validate: int | str) -> bool:  # TODO: Add class as accepted input type
    """
    Validate a PyThings error code.
    :param code_to_validate: the error code to validate.
    :return: **True** if the error code is valid.
    """


# TODO: Create class for error codes

class PyThingsException(Exception):  # TODO: Add hooks
    def __init__(self,
                 message: str = None,
                 code: str | int = None):
        if message is None:
            message = 'An unknown error occurred in PyThings.'
        super().__init__(message)
        self.message = message
        self.code = code if code else 0
        self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp}] E{self.code}]: {self.message}"  # TODO: Make message components dynamic


if __name__ =='__main__':
    pass