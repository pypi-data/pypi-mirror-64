from italian_csv_type_prediction.simple_types import is_euro
from .utils import default_test


def test_is_euro():
    default_test(is_euro, ["Euro"], black_list=[
                 "CAP", "Integer", "Year", "IVA", "NaN", "HouseNumber"])
