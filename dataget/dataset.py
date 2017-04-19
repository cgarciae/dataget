#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa07be40a

# Compiled with Coconut version 1.2.2-post_dev12 [Colonel]

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
import shutil
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

DATASETS = {}

def get_path(path=None, global_=False):
    if global_:
        path = os.environ.get("DATAGET_HOME", None) if os.environ.get("DATAGET_HOME", None) else os.path.expanduser("~/.dataget")
        path = os.path.join(path, "data")
    elif not path:
        path = os.path.join(os.getcwd(), ".dataget", "data")

    return path

def data(dataset_name, path=None, global_=False):

    path = get_path(path=path, global_=global_)

    dataset_class = DATASETS.get(dataset_name, None)
    dataset = dataset_class(dataset_name, path)

    if not dataset:
        raise Exception("Dataset {} does not exist".format(dataset_name))

    return dataset


def ls(installed=False, path=None, global_=False):
    if installed:
        path = get_path(path=path, global_=global_)
        [print(s) for s in os.listdir(path) if (os.path.isdir)(os.path.join(path, s))]
    else:
        [print(s) for s in DATASETS.keys()]


class DataSet(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, home_path):
        self.name = name
        self.path = os.path.join(home_path, self.name)
        self.training_set = self.training_set_class(self)
        self.test_set = self.test_set_class(self)


    def get(self, clear=False, remove_compressed=True, process=True, remove_raw=True, **kwargs):
# clear
        if clear:
            self.clear()

# return if path exists, dataset downloaded already, else create path
        if not self.is_empty():
            return self

# get data
        self.download(**kwargs).extract(**kwargs)

# clean
        if remove_compressed:
            self.remove_compressed(**kwargs)

# process
        if process:
            self.process(**kwargs)

            if remove_raw:
                self.remove_raw()

        return self


    def download(self, clear=False, **kwargs):
# clear
        if clear:
            self.clear()

        if not self.is_empty():
            return self
        elif not self.path_exists():
            os.makedirs(self.path)

        self._download(**kwargs)

        return self

    def extract(self, **kwargs):
        self._extract(**kwargs)

        return self

    def remove_compressed(self, **kwargs):
        self._remove_compressed(**kwargs)

        return self

    def process(self, **kwargs):
        self._process(**kwargs)

        return self

    def remove_raw(self, **kwargs):
        self._remove_raw(**kwargs)

        return self


    def clear(self):
        shutil.rmtree(self.path)

        return self

    @_coconut_tco
    def path_exists(self):
        raise _coconut_tail_call(os.path.exists, self.path)

    def is_empty(self):
        if not self.path_exists():
            return True
        else:
            return not os.listdir(self.path)


    @abstractproperty
    def training_set_class(self):
        pass

    @abstractproperty
    def test_set_class(self):
        pass

    @abstractproperty
    def help(self):
        pass

    @abstractmethod
    def _download(self):
        pass

    @abstractmethod
    def _extract(self):
        pass

    @abstractmethod
    def _remove_compressed(self):
        pass

    @abstractmethod
    def _process(self):
        pass

    @abstractmethod
    def _remove_raw(self):
        pass

    @abstractmethod
    def reqs(self, **kwargs):
        pass


class SubSet(object):
    __metaclass__ = ABCMeta

    def __init__(self, dataset, name):
        self.dataset = dataset
        self.path = os.path.join(dataset.path, name)

    def make_dirs(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    @abstractmethod
    def dataframe(self):
        pass

    @abstractmethod
    def arrays(self):
        pass

    @abstractmethod
    def random_batch_dataframe_generator(self, batch_size):
        pass

    @abstractmethod
    def random_batch_arrays_generator(self, batch_size):
        pass

class TrainingSet(SubSet):

    def __init__(self, dataset):
        super(TrainingSet, self).__init__(dataset, "training-set")


class TestSet(SubSet):

    def __init__(self, dataset):
        super(TestSet, self).__init__(dataset, "test-set")
