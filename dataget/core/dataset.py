from __future__ import print_function, absolute_import, unicode_literals, division
import os
import shutil
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from copy import copy
import pandas as pd
import numpy as np


class DataSet(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self._df = None


    def make_dirs(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)


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
                self.rm_raw(**kwargs)

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
            print(self.path.split("/")[-1])
            shutil.rmtree(self.path)

        return self

    def is_empty(self):
        if not os.path.exists(self.path):
            return True
        else:
            return not os.listdir(self.path)

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
        pass

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

    @abstractmethod
    def get_df(self):
        pass

    @property
    def df(self):
        if self._df is None:
            self._df = self.get_df()
        
        return self._df