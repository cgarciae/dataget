from __future__ import print_function, absolute_import, unicode_literals, division

import os
from .utils import upper_to_dashed

DATASETS = {}

def register_dataset(cls):

    name = upper_to_dashed(cls.__name__)
    DATASETS.update({name: cls})

    return cls

def get_path(name, path=None, global_=False, path_root=None):
    if path:
        return os.path.realpath(path)

    elif global_ or path_root:

        if path_root:
            path = path_root

        elif os.environ.get("DATAGET_HOME", None):
            path = os.environ.get("DATAGET_HOME")

        else:
            path = os.path.expanduser(os.path.join("~", ".dataget")) 
        
        path = os.path.join(path, "data")

    elif os.environ.get("DATAGET_HOME", None):
        path = os.environ.get("DATAGET_HOME")
        path = os.path.join(path, "data")
    else:
        path = os.path.join(os.getcwd(), ".dataget", "data")

    path = os.path.realpath(path)

    if name:
        path = os.path.join(path, name)

    return path

def data(dataset_name, path=None, global_=False, path_root=None, **kwargs):

    path = get_path(dataset_name, path=path, global_=global_, path_root=path_root)

    if dataset_name not in DATASETS:
        raise Exception("Dataset '{}' not found".format(dataset_name))
    
    dataset_class = DATASETS[dataset_name]

    dataset = dataset_class(dataset_name, path, **kwargs)

    return dataset


def ls(available=False, path=None, global_=False, path_root=None):
    
    if available:
        for element in DATASETS.keys():
            print(element)

    else:
        path = get_path(None, path=path, global_=global_, path_root=path_root)

        if not os.path.exists(path):
            return

        for element in os.listdir(path):
            element_path = os.path.join(path, element)

            if os.path.isdir(element_path):
                print(element)
