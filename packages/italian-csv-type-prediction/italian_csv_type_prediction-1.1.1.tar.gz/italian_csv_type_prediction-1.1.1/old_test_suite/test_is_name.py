from italian_csv_type_prediction.simple_types import is_name
from .utils import default_test


def test_is_name():
    default_test(is_name, ["Name"], black_list=["Region", "ProvinceCode",
                                                "Country", "CountryCode", "Surname", "NaN", "Municipality", "String"])
