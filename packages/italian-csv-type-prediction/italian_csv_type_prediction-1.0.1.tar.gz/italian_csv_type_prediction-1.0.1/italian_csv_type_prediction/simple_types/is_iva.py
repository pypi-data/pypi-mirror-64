from .is_nan import is_nan

def is_iva(candidate) -> bool:
    """Return boolean representing if given candidate is a Partita IVA."""
    if is_nan(candidate):
        return False
    candidate = str(candidate)
    if candidate.startswith("IT"):
        candidate = candidate[2:]
    if not candidate.isdigit():
        return False
    try:
        vat_number_check_digit(candidate[0:10])
        return True
    except ValueError:
        return False


def vat_number_check_digit(vat_number):
    """Calculate Italian VAT number check digit."""
    normalized_vat_number = str(vat_number).zfill(10)
    total = 0
    for i in range(0, 10, 2):
        total += int(normalized_vat_number[i])
    for i in range(1, 11, 2):
        quotient, remainder = divmod(int(normalized_vat_number[i]) * 2, 10)
        total += quotient + remainder
    return str((10 - total % 10) % 10)
