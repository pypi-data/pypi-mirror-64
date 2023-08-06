from italian_csv_type_prediction.simple_types import is_cap
from .utils import default_test


def test_is_cap():
    default_test(is_cap, ["CAP"], black_list=["Year", "Integer", "Float", "HouseNumber"])