#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf65fbd40

# Compiled with Coconut version 1.2.3 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------

import os
from .utils import upper_to_dashed

DATASETS = {}

def register_dataset(cls):

    name = upper_to_dashed(cls.__name__)
    DATASETS.update({name: cls})

    return cls

def get_path(path=None, global_=False, path_root=None):
    if path:
        return path

    elif global_ or path_root:
        path = path_root if path_root else os.environ.get("DATAGET_HOME", None) if os.environ.get("DATAGET_HOME", None) else (os.path.expanduser)(os.path.join("~", ".dataget"))
        path = os.path.join(path, "data")

    elif os.environ.get("DATAGET_HOME", None):
        path = (_coconut_partial(os.path.join, {1: "data"}, 2))(os.environ.get("DATAGET_HOME"))
    else:
        path = os.path.join(os.getcwd(), ".dataget", "data")

    path = os.path.realpath(path)

    return path

def data(dataset_name, path=None, global_=False, path_root=None, **kwargs):

    path = get_path(path=path, global_=global_, path_root=path_root)

    dataset_class = DATASETS.get(dataset_name, None)
    dataset = dataset_class(dataset_name, path, **kwargs)

    if not dataset:
        raise Exception("Dataset {} does not exist".format(dataset_name))

    return dataset


def ls(available=False, path=None, global_=False, path_root=None):

    if available:
        [print(s) for s in DATASETS.keys()]

    else:
        path = get_path(path=path, global_=global_, path_root=path_root)

        if not os.path.exists(path):
            return

        [print(s) for s in os.listdir(path) if (os.path.isdir)(os.path.join(path, s))]
