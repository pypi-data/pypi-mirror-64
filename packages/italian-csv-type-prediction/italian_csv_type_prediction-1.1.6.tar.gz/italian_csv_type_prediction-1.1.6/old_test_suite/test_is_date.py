from italian_csv_type_prediction.simple_types import is_date
from .utils import default_test


def test_is_date():
    default_test(is_date, ["Date"], black_list=["CAP", "Year", "Name", "Surname", "String", "HouseNumber"])
