import compress_json
import os

datasets = {}


def load_local_json_sets(path: str):
    if path not in datasets:
        datasets[path] = set(compress_json.load("{pwd}/{path}.json.gz".format(
            pwd=os.path.dirname(os.path.abspath(__file__)),
            path=path
        )))
    return datasets[path]


def load_nan():
    return load_local_json_sets("nan")


def load_provinces_codes():
    return load_local_json_sets("ProvinceCode")


def load_regions():
    return load_local_json_sets("Region")


def load_municipalities():
    return load_local_json_sets("Municipality")


def load_countries():
    return load_local_json_sets("Country")


def load_country_codes():
    return load_local_json_sets("CountryCode")


def load_surnames():
    return load_local_json_sets("Surname")


def load_names():
    return load_local_json_sets("Name")


def load_caps():
    return load_local_json_sets("CAP")


def load_codice_fiscale():
    return load_local_json_sets("CodiceFiscale")


def load_iva():
    return load_local_json_sets("IVA")


def load_strings():
    return load_local_json_sets("String")


def load_email():
    return load_local_json_sets("email")


def load_phone():
    return load_local_json_sets("phone")


def load_euro():
    return load_local_json_sets("euro")


def load_date():
    return load_local_json_sets("date")


def load_address():
    return load_local_json_sets("Address")


def load_house_number():
    return load_local_json_sets("HouseNumber")
