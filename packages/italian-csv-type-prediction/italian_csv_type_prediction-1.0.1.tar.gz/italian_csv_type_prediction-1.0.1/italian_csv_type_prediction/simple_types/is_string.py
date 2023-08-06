from .is_nan import is_nan
from .is_integer import is_integer
from .is_float import is_float
from .is_name import is_name
from .is_surname import is_surname


def is_string(candidate):
    if not isinstance(candidate, str):
        return False
    if any(test(candidate) for test in (is_nan, is_integer, is_float, is_name, is_surname)):
        return False
    return True
