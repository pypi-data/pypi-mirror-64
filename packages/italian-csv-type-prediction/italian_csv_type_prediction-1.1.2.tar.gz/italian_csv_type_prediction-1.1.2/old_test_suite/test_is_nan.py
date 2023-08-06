from italian_csv_type_prediction.simple_types import is_nan
from .utils import default_test
import pytest


def test_is_nan():
    default_test(is_nan, ["NaN"], black_list=["CountryCode"])

    with pytest.raises(ValueError):
        is_nan({})