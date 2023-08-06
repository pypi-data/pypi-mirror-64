from .integer_type import IntegerType
from .regex_type_predictor import RegexTypePredictor


class CAPType(IntegerType):

    def __init__(self):
        """Create new float type predictor based on regex."""
        super().__init__()
        self._predictor = RegexTypePredictor(r"^\d{5}$")

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for CAP values."""
        return super().validate(candidate, **kwargs) and self._predictor.validate(candidate)