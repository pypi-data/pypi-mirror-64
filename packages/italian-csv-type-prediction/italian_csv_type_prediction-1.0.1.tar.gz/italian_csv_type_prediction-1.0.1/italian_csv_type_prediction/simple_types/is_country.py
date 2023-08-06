from ..datasets import load_countries
from ..utils import normalize_string


def is_country(candidate) -> bool:
    """Return boolean representing if given candidate is a valid country."""
    return isinstance(candidate, str) and load_countries() > set((normalize_string(candidate).lower(),))
