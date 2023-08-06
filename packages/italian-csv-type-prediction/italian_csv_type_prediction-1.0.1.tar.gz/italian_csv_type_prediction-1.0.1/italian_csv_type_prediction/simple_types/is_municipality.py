from ..datasets import load_municipalities
from ..utils import normalize_string


def is_municipality(candidate) -> bool:
    """Return boolean representing if given candidate is a valid italian region."""
    return isinstance(candidate, str) and load_municipalities() > set((normalize_string(candidate).upper(),))
