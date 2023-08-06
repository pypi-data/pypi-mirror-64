from codicefiscale import codicefiscale

def is_cf(candidate)->bool:
    """Return boolean representing if given candidate is a Codice Fiscale."""
    return isinstance(candidate, str) and codicefiscale.is_valid(candidate)