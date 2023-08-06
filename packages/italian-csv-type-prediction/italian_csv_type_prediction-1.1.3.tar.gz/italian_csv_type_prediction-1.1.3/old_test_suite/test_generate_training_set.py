from italian_csv_type_prediction.models.tree import generate_training_set


def test_generate_training_set():
    generate_training_set(subsets_number=1)
