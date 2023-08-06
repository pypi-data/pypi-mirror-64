def is_year(candidate):
    try:
        if isinstance(candidate, (str, int)) and str(int(candidate)) == str(candidate):
            candidate = int(candidate)
            if candidate > 1900 and candidate < 2100 or candidate > 0 and candidate < 100:
                return True
    except ValueError:
        pass
    return False