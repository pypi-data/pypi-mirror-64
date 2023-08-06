from ..datasets import load_surnames
from ..utils import normalize_string
from codicefiscale import codicefiscale


def is_surname(candidate, codice_fiscale: str = None) -> bool:
    """Return boolean representing if given candidate is a valid italian surname."""
    if not isinstance(candidate, str):
        return False
    if codice_fiscale is None:
        return load_surnames() > set((normalize_string(candidate).lower(),))
    surname_characters = codicefiscale.decode(codice_fiscale)["raw"]["surname"]
    return all(
        character in candidate.lower()
        for character in surname_characters.rstrip("X").lower()
    )
