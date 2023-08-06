from stdnum import get_cc_module
from .simple_type import SimpleTypePredictor


class IVAType(SimpleTypePredictor):
    def __init__(self):
        """Create new IVA type predictor based on rules."""
        super().__init__()
        self._vat_predictor = get_cc_module('it', 'iva')

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is an IVA."""
        return self._vat_predictor.is_valid(candidate)
