from dateutil.parser import parse
from dateutil.parser import parserinfo
from .is_integer import is_integer
from .is_float import is_float
from .is_name import is_name
from .is_surname import is_surname
from .is_nan import is_nan


class ItalianMonths(parserinfo):

    ITALIAN_MONTHS = [
        ("Gen", "Gennaio"),
        ("Feb", "Febbraio"),
        ("Mar", "Marzo"),
        ("Apr", "Aprile"),
        ("Giu", "Giugno"),
        ("Lug", "Luglio"),
        ("Ago", "Agosto"),
        ("Set", "Settembre"),
        ("Ott", "Ottobre"),
        ("Nov", "Novembre"),
        ("Dic", "Dicembre")
    ]

    MONTHS = [
        (*english, *italian)
        for english, italian in zip(parserinfo.MONTHS, ITALIAN_MONTHS)
    ]


def is_date(candidate, fuzzy=False):
    """
    Return whether the candidate can be interpreted as a date.

    :param candidate: str, candidate to check for date
    :param fuzzy: bool, ignore unknown tokens in candidate if True
    """
    if any(test(candidate) for test in (is_nan, is_integer, is_float, is_name, is_surname)):
        return False
    try:
        parse(candidate, fuzzy=fuzzy, parserinfo=ItalianMonths())
        return True
    except Exception:
        return False
