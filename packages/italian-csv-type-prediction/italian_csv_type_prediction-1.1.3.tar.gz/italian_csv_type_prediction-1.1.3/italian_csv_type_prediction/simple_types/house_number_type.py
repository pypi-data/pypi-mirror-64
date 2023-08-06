from .regex_type_predictor import RegexTypePredictor
from .string_type import StringType


class HouseNumberType(StringType):

    def __init__(self):
        self._predictors = (
            RegexTypePredictor(
                r"^\d{1,5}[\da-z]{0,5}([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?$"),
            RegexTypePredictor(
                r"^[a-z]{1,5}[\/\\\-][\da-z]{0,6}([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?([\/\\\-][\da-z]{0,6})?$")
        )

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if candidate may be an italian house number."""
        return super().validate(candidate) and any(
            predictor.validate(candidate)
            for predictor in self._predictors
        )
