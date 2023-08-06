from stdnum import get_cc_module
from .integer_type import IntegerType


class IVAType(IntegerType):
    def __init__(self):
        """Create new IVA type predictor based on rules."""
        super().__init__()
        self._vat_predictor = get_cc_module('it', 'iva')

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is an IVA."""
        return super().validate(candidate, **kwargs) and self._vat_predictor.is_valid(candidate)
