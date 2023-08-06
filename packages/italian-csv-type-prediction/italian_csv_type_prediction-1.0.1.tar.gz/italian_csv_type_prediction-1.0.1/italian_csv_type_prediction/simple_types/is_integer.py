def is_integer(candidate):
    try:
        return str(int(candidate)) == str(candidate)
    except (ValueError, TypeError):
        return False