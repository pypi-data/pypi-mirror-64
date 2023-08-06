from italian_csv_type_prediction.simple_types import is_address
from .utils import default_test


def test_is_address():
    default_test(is_address, ["Address"])
