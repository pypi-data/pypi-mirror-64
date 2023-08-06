from ..datasets import load_nan
import pandas as pd


def is_nan(candidate) -> bool:
    """Return boolean representing if given candidate is a NaN."""
    if isinstance(candidate, (int, float)):
        return candidate == 0 or pd.isna(candidate)
    if candidate is None:
        return True
    if isinstance(candidate, str):
        return load_nan() > set(candidate) or any(
            e == candidate
            for e in load_nan()
        )
    raise ValueError(
        "Currently unable to handle object of type {}.".format(type(candidate)))
