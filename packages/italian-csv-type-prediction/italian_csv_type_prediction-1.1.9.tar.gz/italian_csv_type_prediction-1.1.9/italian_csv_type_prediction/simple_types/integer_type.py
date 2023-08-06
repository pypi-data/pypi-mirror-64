from .float_type import FloatType


class IntegerType(FloatType):

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate can be considered integer."""
        return super().validate(candidate, **kwargs) and float(str(candidate).replace(",", ".")).is_integer()
