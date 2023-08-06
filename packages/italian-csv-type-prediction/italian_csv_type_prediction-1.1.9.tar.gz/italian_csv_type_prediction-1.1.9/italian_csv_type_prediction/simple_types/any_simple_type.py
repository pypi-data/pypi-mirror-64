from typing import Dict
from .address_type import AddressType
from .CAP_type import CAPType
from .codice_fiscale_type import CodiceFiscaleType
from .country_code_type import CountryCodeType
from .country_type import CountryType
from .currency_type import CurrencyType
from .date_type import DateType
from .email_type import EMailType
from .float_type import FloatType
from .integer_type import IntegerType
from .IVA_type import IVAType
from .municipality_type import MunicipalityType
from .name_type import NameType
from .nan_type import NaNType
from .phone_number_type import PhoneNumberType
from .province_code_type import ProvinceCodeType
from .region_type import RegionType
from .string_type import StringType
from .surname_type import SurnameType
from .biological_sex_type import BiologicalSexType
from .year_type import YearType


class AnySimpleTypePredictor:
    def __init__(self):
        self._predictors = {
            predictor.__name__[:-4]: predictor()
            for predictor in (
                AddressType, CAPType, CodiceFiscaleType, CountryCodeType,
                CountryType, CurrencyType, DateType, EMailType,
                FloatType, IntegerType, IVAType,
                MunicipalityType, NameType, NaNType, PhoneNumberType,
                ProvinceCodeType, RegionType, StringType, SurnameType,
                YearType, BiologicalSexType
            )
        }

    def supported_types(self):
        """Return list of currently supported types."""
        return list(self._predictors.keys())

    def predict(self, candidate, **kwargs) -> Dict[str, bool]:
        """Return prediction from all available type."""
        return {
            key: predictor.validate(candidate)
            for key, predictor in self._predictors.items()
        }
