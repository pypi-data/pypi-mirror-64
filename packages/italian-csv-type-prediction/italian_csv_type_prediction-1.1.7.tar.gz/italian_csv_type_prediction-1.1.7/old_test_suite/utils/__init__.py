import numpy as np
from italian_csv_type_prediction.models.tree import datasets
from typing import List

datasets_corner_cases = {
    "NaN": ["", 0, "Nan", ".", "-", np.nan, None],
    "CAP": ["29121", "00121", 561, 29121, 29121.00],
    "ProvinceCode": ["pc", "re"],
    "Region": ["Emilia-romagna", "valle d'aosta"],
    "Municipality": ["Piacenza", "Ferriere"],
    "CodiceFiscale": ["BNCBBR69B58L219S", "SMPFBA87H03C722E", "HMDSRS66S65Z336A"],
    "Year": ["1999", "2010", 2017, 2030, 97, 17, 15],
    "Country": ["italia", "Italia"],
    "CountryCode": ["DE", "IT", "it", "fr"],
    "Name": ["luca", "sara", "marco", "carlo", "giovanni", "noemi", "xiaoxiao", "xiao", "ali"],
    "Surname": ["cappelletti", "bonfitto", "mesiti", "angelucci", "deda", "li", "fontana"],
    "IVA": ["00380210302", "02005780131", "02437800135", "IT02437800135", 2437800135],
    "Date": ["12/12/1994", "12 dicembre 1994", "12 dic 1994"]
}

types = {
    key: list(value) + list(datasets_corner_cases[key]
                  if key in datasets_corner_cases else [])
    for key, value in datasets.items()
}


def get_type(t):
    return types[t]


def get_not_type(t):
    return [
        e
        for key, elements in types.items()
        if key != t
        for e in elements
    ]


def get_cases(t):
    return get_type(t), get_not_type(t)


def default_test(test, positives: List[str], negatives: List[str] = (), black_list: List[str] = ()):
    for e in list(positives) + list(negatives) + list(black_list):
        if e not in types:
            raise ValueError("Given type {} is not available!".format(e))

    if not negatives:
        negatives = list(set(types.keys()) - set(positives) - set(black_list))

    for pos in positives:
        for t in types[pos]:
            if not test(t):
                raise AssertionError("Test {testname} on {positive} from {key} has failed.".format(
                    testname=test.__name__,
                    key=pos,
                    positive=t
                ))

    for neg in negatives:
        for t in types[neg]:
            if test(t):
                raise AssertionError("Test {testname} on {negative} from {key} has failed.".format(
                    testname=test.__name__,
                    key=neg,
                    negative=t
                ))
