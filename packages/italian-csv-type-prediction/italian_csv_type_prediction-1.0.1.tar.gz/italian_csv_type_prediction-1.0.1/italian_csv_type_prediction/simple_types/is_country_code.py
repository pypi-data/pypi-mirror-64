from ..datasets import load_country_codes
from ..utils import normalize_string


def is_country_code(candidate) -> bool:
    """Return boolean representing if given candidate is a valid country code."""
    return isinstance(candidate, str) and load_country_codes() > set((normalize_string(candidate).upper(),))
