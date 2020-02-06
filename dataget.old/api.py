from __future__ import print_function, absolute_import, unicode_literals, division

import os
from .utils import upper_to_dashed, get_path


DATASETS = {}


def register_dataset(cls):

    name = upper_to_dashed(cls.__name__)
    DATASETS.update({name: cls})

    return cls



def data(dataset_name, path=None, **kwargs):

    path = get_path(dataset_name, path=path)

    if dataset_name not in DATASETS:
        raise Exception("Dataset '{}' not found".format(dataset_name))
    
    dataset_class = DATASETS[dataset_name]

    dataset = dataset_class(dataset_name, path, **kwargs)

    return dataset


def ls(installed=False):
    
    if installed:
        path = get_path()

        if not os.path.exists(path):
            return []


        datasets = os.listdir(path)
        datasets = map(lambda folder: os.path.join(path, folder), datasets)
        datasets = filter(os.path.isdir, datasets)
        datasets = list(datasets)

        return datasets

    else:
        return DATASETS.keys()
