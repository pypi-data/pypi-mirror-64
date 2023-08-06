from italian_csv_type_prediction.simple_types import is_year
from .utils import default_test


def test_is_year():
    default_test(is_year, ["Year"], black_list=["CAP", "Integer", "HouseNumber"])
