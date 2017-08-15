#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xcb46fdbc

# Compiled with Coconut version 1.2.3-post_dev5 [Colonel]

# Coconut Header: --------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------------

import os
from platform import python_version
from dataget import get_path
from dataget.dataset import DataSet
import platform


def load_datasets(DATASETS, module_root, datasets_path):
    if not os.path.exists(datasets_path):
        return

    datasets = ((_coconut.functools.partial(map, _coconut.operator.methodcaller("replace", ".py", "")))((_coconut.functools.partial(filter, lambda x: not x.startswith("_")))((_coconut.functools.partial(filter, _coconut.operator.methodcaller("endswith", ".py")))(os.listdir(datasets_path)))))

    for dataset in datasets:
        module_name = (_coconut.functools.partial("{}.{}".format, module_root))(dataset.replace("-", "_"))
        filename = (_coconut.functools.partial(os.path.join, datasets_path))("{}.py".format(dataset))

        load_module(module_name, filename)




def load_custom_datasets(DATASETS):
    splitter = "/" if not platform.system() == "Windows" else "\\"

    datasets_path = ((_coconut_partial(os.path.join, {1: "datasets"}, 2))((splitter.join)((_coconut.operator.itemgetter(_coconut.slice(None, -1)))((_coconut.operator.methodcaller("split", splitter))(__file__)))))

    load_datasets(DATASETS, "datasets", datasets_path)


def load_plugin_datasets(DATASETS):
    datasets_path = os.environ.get("DATAGET_HOME", None) if os.environ.get("DATAGET_HOME", None) else (os.path.expanduser)(os.path.join("~", ".dataget"))
    datasets_path = os.path.join(datasets_path, "datasets")

    load_datasets(DATASETS, "datasets", datasets_path)


def load_local_datasets(DATASETS):

    datasets_path = (_coconut_partial(os.path.join, {1: ".dataget", 2: "datasets"}, 3))(os.getcwd())

    if os.path.exists(datasets_path):
        load_datasets(DATASETS, "datasets", datasets_path)


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
