from ..datasets import load_regions
from ..utils import normalize_string


def is_region(candidate) -> bool:
    """Return boolean representing if given candidate is a valid italian region."""
    return isinstance(candidate, str) and load_regions() > set((normalize_string(candidate).upper(),))
