#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xdc812f79

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
import shutil
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty


class DataSet(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, home_path):
        self.name = name
        self.path = os.path.join(home_path, self.name)
        self.training_set = self.training_set_class(self, "training-set")
        self.test_set = self.test_set_class(self, "test-set")


    def make_dirs(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.training_set.make_dirs()
        self.test_set.make_dirs()


    def before_op(self, **kwargs):
        pass


    def get(self, download=True, rm=False, rm_compressed=True, process=True, rm_raw=True, **kwargs):
        self.before_op(**kwargs)

# rm
        if rm:
            self.rm(**kwargs)

# return if path exists, dataset downloaded already, else create path
        if not self.is_empty():
            return self

# get data
        if download:
            self.download(**kwargs)

        self.extract(**kwargs)

# process
        if process:
            self.process(**kwargs)

            if rm_raw:
                self.rm_raw()

# clean
        if rm_compressed:
            self.rm_compressed(**kwargs)

        return self


    def download(self, rm=False, **kwargs):
        self.before_op(**kwargs)
        print("===DOWNLOAD===")

# rm
        if rm:
            self.rm(**kwargs)

        if not self.is_empty():
            return self


        self.make_dirs()

        self._download(**kwargs)

        print("")

        return self

    def extract(self, **kwargs):
        self.before_op(**kwargs)

        print("===EXTRACT===")

        self.make_dirs()

        self._extract(**kwargs)

        print("")

        return self

    def rm_compressed(self, **kwargs):
        self.before_op(**kwargs)
        print("===RM-COMPRESSED===")

        self._rm_compressed(**kwargs)

        print("")

        return self

    def process(self, **kwargs):
        self.before_op(**kwargs)

        print("===PROCESS===")

        self._process(**kwargs)

        print("")

        return self

    def rm_raw(self, **kwargs):
        self.before_op(**kwargs)
        print("===RM-RAW===")

        self._rm_raw(**kwargs)

        print("")

        return self


    def rm(self, **kwargs):
        self.before_op(**kwargs)

        if os.path.exists(self.path):
            (print)((_coconut.operator.itemgetter(-1))(self.path.split("/")))
            shutil.rmtree(self.path)

        return self

    def rm_subsets(self, **kwargs):
        self.before_op(**kwargs)

        if os.path.exists(self.training_set.path):
            shutil.rmtree(self.training_set.path)

        if os.path.exists(self.test_set.path):
            shutil.rmtree(self.test_set.path)

        return self

    def is_empty(self):
        if not os.path.exists(self.path):
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


    def _rm_compressed(self, **kwargs):
        print("removing compressed files")

        for file in os.listdir(self.path):

            file = os.path.join(self.path, file)

            if not os.path.isdir(file):
                os.remove(file)

    def remove_all_file_with_extension(self, extension):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = os.path.join(root, file)
                if file.endswith(".{}".format(extension)):
                    os.remove(file)

    @abstractmethod
    def _process(self):
        pass

    @abstractmethod
    def _rm_raw(self):
        pass

    @abstractmethod
    def reqs(self, **kwargs):
        pass


class SubSet(object):
    __metaclass__ = ABCMeta

    def __init__(self, dataset, name):
        self.dataset = dataset
        self._name = name

    def make_dirs(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    @property
    def path(self):
        return os.path.join(self.dataset.path, self._name)

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
