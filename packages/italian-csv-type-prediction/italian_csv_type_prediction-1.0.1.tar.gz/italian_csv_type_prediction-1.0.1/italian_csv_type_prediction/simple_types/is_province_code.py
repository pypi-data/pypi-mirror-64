from ..datasets import load_provinces_codes
from ..utils import normalize_string


def is_province_code(candidate) -> bool:
    """Return boolean representing if given candidate is a valid italian province."""
    return isinstance(candidate, str) and load_provinces_codes() > set((normalize_string(candidate).upper(),))
