from italian_csv_type_prediction.simple_types import is_country_code
from .utils import default_test


def test_is_country_code():
    default_test(is_country_code, ["CountryCode"], black_list=[
                 "ProvinceCode", "Municipality", "Name", "Surname", "String", "NaN"])
