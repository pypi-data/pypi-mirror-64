from italian_csv_type_prediction.simple_types import is_house_number
from .utils import default_test


def test_is_house_number():
    default_test(is_house_number, ["HouseNumber"], black_list=["Integer", "Year", "Date", "CAP", "String"])
