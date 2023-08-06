from dateutil.parser import parse
from dateutil.parser import parserinfo
from .string_type import StringType


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


class DateType(StringType):

    def __init__(self):
        """Create new DateType predictor."""
        super().__init__()
        self._parserinfo = ItalianMonths()

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a Date."""
        try:
            parse(candidate, parserinfo=self._parserinfo)
            return True
        except Exception:
            return False
