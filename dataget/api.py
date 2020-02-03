import os
from dataget.utils import upper_to_dashed
from pathlib import Path


DATASETS = {}


def register_dataset(cls):

    name = upper_to_dashed(cls.__name__)

    if name in DATASETS:
        raise ValueError(f"Dataset for '{cls.__name__}' already registered")

    DATASETS[name] = cls

    return cls


def data(dataset_name, path=None, local=False, **kwargs):

    if dataset_name not in DATASETS:
        raise Exception("Dataset '{}' not found".format(dataset_name))

    if path:
        pass
    elif local:
        path = Path("data")
    else:
        path = Path("~").expanduser() / ".dataget"

    dataset = DATASETS[dataset_name](path, **kwargs)

    return dataset


def datasets_list():
    return list(DATASETS.keys())
