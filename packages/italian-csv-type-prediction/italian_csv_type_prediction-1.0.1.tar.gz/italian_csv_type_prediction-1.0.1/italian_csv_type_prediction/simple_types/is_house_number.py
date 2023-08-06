import re
from .is_integer import is_integer
from .is_iva import is_iva

house_number_regex1 = re.compile(
    r"^\d{1,5}[\da-z]{0,5}([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?$"
)
house_number_regex2 = re.compile(
    r"^[a-z]{1,5}[\/\\\-][\da-z]{0,6}([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?$"
)


def is_house_number(candidate) -> bool:
    """Return boolean representing if candidate may be an italian house number.

    Notes
    ------------------------------
    Sestiere is a kind of place in Venetian.

    """
    global house_number_regex1, house_number_regex2
    if is_integer(candidate):
        number = int(candidate)
        return number < 10000 and number>0
    if not isinstance(candidate, str):
        return False
    if is_iva(candidate):
        return False
    candidate = candidate.lower().strip(".n°").replace(" ", "")
    if house_number_regex1.match(candidate):
        return True
    if house_number_regex2.match(candidate):
        return True
    return False
