from ..datasets import (
    load_nan, load_names, load_regions, load_countries, load_country_codes,
    load_municipalities, load_surnames, load_provinces_codes, load_caps,
    load_codice_fiscale, load_iva, load_strings, load_email, load_phone,
    load_date, load_euro, load_address, load_house_number
)
from ..simple_types import is_any_type
import pandas as pd
import numpy as np
import os
import random
import compress_pickle
from typing import List
from tqdm.auto import tqdm

tree = None

datasets = {
    "NaN": tuple(load_nan()),
    "CAP": tuple(load_caps()),
    "ProvinceCode": tuple(load_provinces_codes()),
    "Region": tuple(load_regions()),
    "Municipality": tuple(load_municipalities()),
    "CodiceFiscale": tuple(load_codice_fiscale()),
    "Year": [random.randint(1950, 2050) for _ in range(10000)],
    "Integer": [random.randint(-100000, 100000) for _ in range(10000)],
    "Float": [random.uniform(-100000, 100000) for _ in range(10000)],
    "Country": tuple(load_countries()),
    "CountryCode": tuple(load_country_codes()),
    "Name": tuple(load_names()),
    "Surname": tuple(load_surnames()),
    "IVA": tuple(load_iva()),
    "String": tuple(load_strings()),
    "Email": tuple(load_email()),
    "Phone": tuple(load_phone()),
    "Euro": tuple(load_euro()),
    "Date": tuple(load_date()),
    "Address": tuple(load_address()),
    "HouseNumber": tuple(load_house_number())
}

classes = list(datasets.keys())


def generate_training_set(subsets_number=1000, subsets_elements_number=40, error_probability=0.01):
    items = list(datasets.items())
    X, Y = None, []
    for _ in tqdm(
        range(subsets_number),
        total=subsets_number,
        desc="Generating training dataset"
    ):
        main_dataset_name, dataset = random.choice(items)
        x = []
        for _ in range(subsets_elements_number):
            if random.uniform(0, 1) < 1-error_probability:
                x.append(random.choice(dataset))
                Y.append(main_dataset_name)
            else:
                tmp_dataset_name, tmp_dataset = random.choice(items)
                x.append(random.choice(tmp_dataset))
                Y.append(tmp_dataset_name)
        scores = compute_set_scores(x)
        if X is None:
            X = scores
        else:
            X = np.vstack([
                X,
                scores
            ])
    return X, [
        classes.index(y)
        for y in Y
    ]


def compute_set_scores(x: List[str]):
    df = pd.DataFrame([
        is_any_type(i)
        for i in x
    ])
    means = df.mean().values
    tiled = np.tile(means, (len(x), 1))
    return np.hstack([
        df.values,
        tiled
    ])


def load_tree():
    global tree
    if tree is None:
        tree = compress_pickle.load(
            "{}/tree.pkl.gz".format(os.path.dirname(os.path.abspath(__file__))))
    return tree


def predict_types(x: List[str]) -> List[str]:
    """Return list of types of given list."""
    global classes
    return [
        classes[i]
        for i in load_tree().predict(compute_set_scores(x))
    ]
