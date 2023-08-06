import re
from .is_nan import is_nan

cap_regex = re.compile(r"^\d{5}$")


def is_cap(candidate) -> bool:
    """Return a boolean representing if given candidate is a valid italian CAP."""
    if isinstance(candidate, (str, int, float)):
        try:
            return bool(cap_regex.match(str(int(float(candidate))).zfill(5))) and not is_nan(candidate)
        except (ValueError, OverflowError):
            return False

    return False
