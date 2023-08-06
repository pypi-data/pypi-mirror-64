from italian_csv_type_prediction.simple_types import is_cf
from .utils import default_test


def test_is_cf():
    default_test(is_cf, ["CodiceFiscale"])
