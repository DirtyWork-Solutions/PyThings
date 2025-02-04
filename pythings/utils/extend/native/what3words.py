import os

from pythings.__errors__ import PyThingsExtensionException

"""
Provides native support and integration with the what3words project and API.
"""

def api_key_check():  # TODO: Add check logic and rename method
    """
    TODO: Method docs

    :return:
    """

    #
    if "W3W_API_KEY" not in os.environ.keys():
        raise KeyError("Missing Environment Variable: what3words integration requires 'W3W_API_KEY' be set.")

def coordinates_to_words(coordinates: dict | tuple | str, use_deliminator: str | bool = False) -> tuple | str:  # TODO: Implement logic
    """
    Convert a **longitude** and **latitude** into a **what3words**.

    :param coordinates:
    :param use_deliminator: Use a *comma* as deliminator and return a string instead of tuple
    :return: a tuple or string, if *use_deliminator* is **True**
    """
    try:
        api_key_check()
    except KeyError as e:
        raise PyThingsExtensionException(e)

def words_to_coordinates(words: str | tuple) -> tuple | dict | None:  # TODO: Implement logic
    """
    Convert a **what3words** into a **longitude** and **latitude**.

    :param words:
    :return:
    """
    if isinstance(words, str):
        return None
    elif isinstance(words, tuple):
        return None
    else:
        raise TypeError(f"{str(type(words))} is unsupported: 'Words' must come as a deliminated string or tuple.")
