from validate_email import validate_email


def is_email(candidate)->bool:
    """Return boolean representing if given candidate is an email."""
    return isinstance(candidate, str) and validate_email(candidate)