from .is_nan import is_nan

def is_float(candidate):
    try:
        return str(float(candidate)) == str(candidate) and not is_nan(candidate)
    except (ValueError, TypeError):
        return False