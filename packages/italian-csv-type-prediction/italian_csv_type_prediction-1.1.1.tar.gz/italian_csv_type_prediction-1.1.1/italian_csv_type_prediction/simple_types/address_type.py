from .string_type import StringType
from ..datasets import load_address_starters


class AddressType(StringType):

    def __init__(self):
        super().__init__()
        self._starters = load_address_starters()

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if candidate may be an italian address."""
        return super().validate(candidate) and any(candidate.lower().startswith(start+" ") for start in self._starters)
