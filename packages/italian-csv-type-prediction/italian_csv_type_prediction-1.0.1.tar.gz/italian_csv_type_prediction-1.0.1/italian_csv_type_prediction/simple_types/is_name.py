from ..datasets import load_names
from ..utils import normalize_string
from codicefiscale import codicefiscale


def is_name(candidate, codice_fiscale: str = None) -> bool:
    """Return boolean representing if given candidate is a valid italian name."""
    if not isinstance(candidate, str):
        return False
    if codice_fiscale is None:
        return load_names() > set((normalize_string(candidate).lower(),))
    name_characters = codicefiscale.decode(codice_fiscale)["raw"]["name"]
    return all(
        character in candidate.lower()
        for character in name_characters.rstrip("X").lower()
    )
