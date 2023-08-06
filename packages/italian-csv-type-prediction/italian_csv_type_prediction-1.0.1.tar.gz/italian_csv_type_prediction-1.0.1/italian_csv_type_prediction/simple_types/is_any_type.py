from typing import Dict
from .is_nan import is_nan
from .is_cap import is_cap
from .is_date import is_date
from .is_province_code import is_province_code
from .is_region import is_region
from .is_municipality import is_municipality
from .is_iva import is_iva
from .is_cf import is_cf
from .is_year import is_year
from .is_country import is_country
from .is_country_code import is_country_code
from .is_name import is_name
from .is_surname import is_surname
from .is_euro import is_euro
from .is_float import is_float
from .is_integer import is_integer
from .is_string import is_string
from .is_email import is_email
from .is_phone import is_phone
from .is_address import is_address
from .is_house_number import is_house_number

types = {
    "NaN": is_nan,
    "CAP": is_cap,
    "Date": is_date,
    "ProvinceCode": is_province_code,
    "Region": is_region,
    "Municipality": is_municipality,
    "IVA": is_iva,
    "CodiceFiscale": is_cf,
    "Year": is_year,
    "Country": is_country,
    "CountryCode": is_country_code,
    "Name": is_name,
    "Surname": is_surname,
    "Euro": is_euro,
    "Float": is_float,
    "Integer": is_integer,
    "String": is_string,
    "Email": is_email,
    "Phone": is_phone,
    "Address": is_address,
    "HouseNumber": is_house_number
}


def is_any_type(candidate) -> Dict[str, bool]:
    """Return dictionary of predicted types."""
    return {
        key: test(candidate.strip() if isinstance(candidate, str) else candidate)
        for key, test in types.items()
    }