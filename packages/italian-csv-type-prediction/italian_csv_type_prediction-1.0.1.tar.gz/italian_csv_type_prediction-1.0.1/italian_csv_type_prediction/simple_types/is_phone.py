import phonenumbers

def is_phone(candidate)->bool:
    """Return boolean representing if given candidate is a phone number."""
    candidate = str(candidate)
    try:
        return phonenumbers.is_valid_number(phonenumbers.parse(candidate, "IT"))
    except phonenumbers.NumberParseException:
        return False