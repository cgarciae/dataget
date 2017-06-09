#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x58feeb11

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

import urllib
import zipfile
import os
import shutil
from dataget.utils import get_file
from dataget.dataset import ImageDataSetWithMetadata
from dataget.api import register_dataset
from multiprocessing import Pool
from dataget.utils import OS_SPLITTER

TRAINING_SET_URL = "http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Training_Images.zip"
TEST_SET_URL = "http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_Images.zip"
TEST_CSV_URL = "http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_GT.zip"

@register_dataset
class GermanTrafficSigns(ImageDataSetWithMetadata):

    def __init__(self, *args, **kwargs):
        super(GermanTrafficSigns, self).__init__(*args, **kwargs)

        self._training_images_path = os.path.join(self.training_set.path, "GTSRB/Final_Training/Images")
        self._test_images_path = os.path.join(self.test_set.path, "GTSRB/Final_Test/Images")


    @property
    def _raw_extension(self):
        return "ppm"

    @property
    def help(self):
        return "TODO"

    def reqs(self, **kwargs):
        return super(GermanTrafficSigns, self).reqs() + ""


    def _download(self, **kwargs):
        get_file(TRAINING_SET_URL, self.path, "training-set.zip")
        get_file(TEST_CSV_URL, self.path, "test-set.csv.zip")
        get_file(TEST_SET_URL, self.path, "test-set.zip")

    def _extract_training_set(self, **kwargs):
        import pandas as pd

        print("extracting training-set.zip")
        with zipfile.ZipFile(os.path.join(self.path, "training-set.zip"), 'r') as zip_ref:
            for file in zip_ref.namelist():


# skip directories
                if os.path.basename(file):

                    if file.endswith(".csv") or file.endswith(self.raw_extension):
# print(file)
# print(self.path)
# os.path.join(self.path, file) |> print
                        structure = (_coconut.operator.methodcaller("split", "/"))(file)
                        filename = structure[-1]
                        class_id = (str)((int)(structure[-2]))


                        if not (os.path.exists)(os.path.join(self.training_set.path, class_id)):
                            (os.makedirs)(os.path.join(self.training_set.path, class_id))

                        if file.endswith(".csv"):
                            filename = "{}.csv".format(class_id)


# copy file (taken from zipfile's extract)
                        path = os.path.join(self.training_set.path, class_id, filename)
                        source = zip_ref.open(file)
                        target = open(path, "wb")

                        with source, target:
                            shutil.copyfileobj(source, target)

                        if file.endswith(".csv"):
                            df = pd.read_csv(path, sep=";")
                            df.columns = (list)((_coconut.functools.partial(map, _coconut.operator.methodcaller("lower")))(df.columns))
                            df.rename(columns={'classid': 'class_id'}, inplace=True)
                            df.to_csv(path, index=False)



    def _extract_test_set(self, **kwargs):
        print("extracting test-set.zip")
        with zipfile.ZipFile(os.path.join(self.path, "test-set.zip"), 'r') as zip_ref:
            for file in zip_ref.namelist():
# skip directories
                if os.path.basename(file):

                    if file.endswith(self.raw_extension):
                        structure = (_coconut.operator.methodcaller("split", "/"))(file)
                        filename = structure[-1]
                        path = os.path.join(self.test_set.path, filename)

# copy file (taken from zipfile's extract)
                        source = zip_ref.open(file)
                        target = open(path, "wb")

                        with source, target:
                            shutil.copyfileobj(source, target)

        print("extracting test-set.csv.zip")
        with (_coconut_partial(zipfile.ZipFile, {1: 'r'}, 2))(os.path.join(self.path, "test-set.csv.zip")) as zip_ref:
            path = os.path.join(self.test_set.path, "test-set.csv")

# copy file (taken from zipfile's extract)
            source = zip_ref.open("GT-final_test.csv")
            target = open(path, "wb")

            with source, target:
                shutil.copyfileobj(source, target)

            with (_coconut_partial(open, {1: "r"}, 2))(os.path.join(self.test_set.path, "test-set.csv")) as f:
                txt = f.read().replace(";", ",")

            with (_coconut_partial(open, {1: "w"}, 2))(os.path.join(self.test_set.path, "test-set.csv")) as f:
                f.write(txt)



        self._structure_folder_from_csv(self.test_set.path)

#remove old csv
        (os.remove)(os.path.join(self.test_set.path, "test-set.csv"))


    def _structure_folder_from_csv(self, dir_path):
        import pandas as pd

        print("organizing test-set")

        csv_files = (_coconut.functools.partial(map, _coconut.functools.partial(os.path.join, dir_path)))((_coconut.functools.partial(filter, _coconut.operator.methodcaller("endswith", ".csv")))(os.listdir(dir_path)))

        df = (pd.concat)((_coconut.functools.partial(map, pd.read_csv))(csv_files))
        df.columns = (list)((_coconut.functools.partial(map, _coconut.operator.methodcaller("lower")))(df.columns))
        df.rename(columns={'classid': 'class_id'}, inplace=True)

        groups = df.groupby(["class_id"])

        for class_id, group in groups:
            group = group.copy()
            class_path = os.path.join(dir_path, str(class_id))
            group_csv_path = os.path.join(class_path, str(class_id)) + ".csv"

            for i, row in group.iterrows():
                file_path = os.path.join(class_path, row.filename)
                current_file_path = os.path.join(dir_path, row.filename)

                if not os.path.exists(class_path):
                    os.makedirs(class_path)

# move files
                os.rename(current_file_path, file_path)


#create group csv
            group.to_csv(group_csv_path, index=False)



    def _extract(self, **kwargs):
        self._extract_training_set(**kwargs)
        self._extract_test_set(**kwargs)


    def process_dataframe(self, dataframe, **kwargs):
# print(dataframe.iloc[0].class_id)
        pass
