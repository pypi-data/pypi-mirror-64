from ..embedding import DataframeEmbedding
import random
import numpy as np
from tqdm.auto import trange
import pandas as pd
from ..datasets import (
    load_nan, load_names, load_regions, load_countries, load_country_codes,
    load_municipalities, load_surnames, load_provinces_codes, load_caps,
    load_codice_fiscale, load_iva, load_strings, load_email, load_phone,
    load_date, load_euro, load_address, load_biological_sex,
)


class SimpleDatasetGenerator:

    def __init__(self):
        self._datasets = self._load_types_datasets()
        self._embedding = DataframeEmbedding()

    def _load_types_datasets(self):
        datasets = {
            "CodiceFiscale": load_codice_fiscale(),
            "IVA": load_iva(),
            "Address": load_address(),
            "CAP": load_caps(),
            "NaN": load_nan(),
            "ProvinceCode": load_provinces_codes(),
            "Region": load_regions(),
            "Municipality": load_municipalities(),
            "Year": [random.randint(1990, 2030) for _ in range(1000)],
            "Integer": [random.randint(-100000, 100000) for _ in range(10000)],
            "Float": [random.uniform(-100000, 100000) for _ in range(10000)],
            "Country": load_countries(),
            "CountryCode": load_country_codes(),
            "Name": load_names(),
            "Surname": load_surnames(),
            "String": load_strings(),
            "EMail": load_email(),
            "PhoneNumber": load_phone(),
            "Currency": load_euro(),
            "Date": load_date(),
            "BiologicalSex": load_biological_sex()
        }

        return {
            key: np.array(value)
            for key, value in datasets.items()
        }

    def generate_simple_dataframe(
        self,
        nan_percentage: float = 0.1,
        min_rows: int = 3,
        max_rows: int = 50,
        mix_codes: bool = True
    ):
        rows = random.randint(min_rows, max_rows)
        df = pd.DataFrame({
            key: np.random.choice(values, size=rows, replace=True)
            for key, values in self._datasets.items()
        })

        types = np.tile(np.array(df.columns), (len(df), 1))

        if mix_codes:
            mask = np.random.randint(0, 2, size=df.shape[0], dtype=bool)
            swap_codice_fiscale = df.CodiceFiscale[mask].values
            swap_iva = df.IVA[mask].values
            df.loc[mask, "CodiceFiscale"] = swap_iva
            df.loc[mask, "IVA"] = swap_codice_fiscale
            types[mask, 0] = "IVA"
            types[mask, 1] = "CodiceFiscale"

        if nan_percentage > 0:
            mask = np.random.choice([False, True], size=df.shape, p=[
                                    nan_percentage, 1-nan_percentage])
            types[np.logical_not(mask)] = "NaN"
            df = df.where(mask)
        return df, types

    def _build(self):
        df, types = self.generate_simple_dataframe()
        return self._embedding.transform(df, types)

    def build(self, number:int=1000):
        """Creates and encodes a number of dataframe samples for training"""
        X, y = list(zip(*[
            self._build()
            for _ in trange(number, desc="Rendering dataset")
        ]))

        return np.vstack(X), np.concatenate(y)