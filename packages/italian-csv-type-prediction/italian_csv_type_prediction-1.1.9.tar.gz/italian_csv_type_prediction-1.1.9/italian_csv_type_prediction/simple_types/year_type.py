from .integer_type import IntegerType


class YearType(IntegerType):

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate can be considered a Year."""
        if super().validate(candidate, **kwargs):
            candidate = int(float(str(candidate).replace(",", ".")))
            return any(
                candidate > _max and candidate < _min
                for _max, _min in ((1990, 2030),)
            )
        return False
