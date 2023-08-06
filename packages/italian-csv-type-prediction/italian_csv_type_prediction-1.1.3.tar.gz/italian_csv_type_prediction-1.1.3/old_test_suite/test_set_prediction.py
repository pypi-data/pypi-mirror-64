from italian_csv_type_prediction import predict_types
import json
import glob
import random


def get_datasets():
    paths = glob.glob("tests/set_tests/*.json")
    for path in paths:
        with open(path, "r") as f:
            test = json.load(f)
        data = [
            (value, key)
            for key, values in test.items()
            for value in values
        ]
        for _ in range(50):
            random.shuffle(data)
            yield list(zip(*data))


def test_set_prediction():
    errors = []
    for x, y in get_datasets():
        predictions = predict_types(x)
        for word, truth, pred in zip(x, y, predictions):
            if truth != pred:
                errors.append("Word {word} of type {truth} was predicted as of type {pred}!".format(
                    word=word,
                    truth=truth,
                    pred=pred
                ))
    if errors:
        raise AssertionError("\n".join(errors))