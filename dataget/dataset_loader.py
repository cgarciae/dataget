from __future__ import absolute_import, print_function, unicode_literals, division

import os
from platform import python_version
from .api import DATASETS


def load_datasets(datasets_path):
    if not os.path.exists(datasets_path):
        return

    datasets = os.listdir(datasets_path)
    datasets = filter(lambda s: s.endswith(".py"), datasets)
    datasets = filter(lambda s: not s.startswith("_"), datasets)
    datasets = map(lambda s: s.replace(".py", ""), datasets)

    for dataset in datasets:
        module_name = dataset.replace("-", "_")
        module_name = "{}.{}".format("datasets", module_name)

        filename = "{}.py".format(dataset)
        filename = os.path.join(datasets_path, filename)

        load_module(module_name, filename)




def load_custom_datasets():

    datasets_path = __file__.split(os.sep)[:-1]
    datasets_path = os.sep.join(datasets_path)
    datasets_path = os.path.join(datasets_path, "datasets")

    load_datasets(datasets_path)


def load_plugin_datasets():
    datasets_path = os.environ.get("DATAGET_HOME", None) if os.environ.get("DATAGET_HOME", None) else os.path.expanduser(os.path.join("~", ".dataget"))
    datasets_path = os.path.join(datasets_path, "datasets")

    load_datasets(datasets_path)


def load_local_datasets():

    datasets_path = os.getcwd()
    datasets_path = os.path.join(datasets_path, ".dataget", "datasets")

    if os.path.exists(datasets_path):
        load_datasets(datasets_path)

def load_datasets_at(path, dataget_folder = True):

    datasets_path = os.path.realpath(path)

    if dataget_folder:
        datasets_path = os.path.join(datasets_path, ".dataget", "datasets")

    if os.path.exists(datasets_path):
        load_datasets(datasets_path)


def load_module(module_name, file_path):
    if python_version() >= "3.5":
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    elif python_version() >= "3":
        from importlib.machinery import SourceFileLoader
        module = SourceFileLoader(module_name, file_path).load_module()

    else:
        import imp
        module = imp.load_source(module_name, file_path)

    return module
