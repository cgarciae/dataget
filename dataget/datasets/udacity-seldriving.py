#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa8386218

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
from dataget.utils import move_files
from dataget.api import register_dataset
from multiprocessing import Pool
from dataget.dataset import ImageNavigationDataSet
import time


URL = "https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584f6edd_data/data.zip"

@register_dataset
class UdacitySelfdrivingSimulator(ImageNavigationDataSet):

    @property
    def features(self):
        return ["image", "speed", "camera"]

    @property
    def labels(self):
        return ["steering", "throttle", "brake", "original_steering"]

    @property
    def _raw_extension(self):
        return "jpg"

    @property
    def help(self):
        return "TODO"

    def reqs(self, **kwargs):
        return super(UdacitySelfdrivingSimulator, self).reqs() + " odo"

    def _download(self, **kwargs):
        get_file(URL, self.path, "dataset.zip")

    def _extract(self, train_size=0.8, **kwargs):
        from odo import odo
        from pandas import DataFrame
        import pandas as pd
        import numpy as np

        print("Extracting zip")
        with zipfile.ZipFile(os.path.join(self.path, "dataset.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.path)

        (_coconut_partial(shutil.move, {1: self.path}, 2))(os.path.join(self.path, "data", "IMG"))
        (_coconut_partial(shutil.move, {1: self.path}, 2))(os.path.join(self.path, "data", "driving_log.csv"))


        print("Loading Data")
        csv_path = os.path.join(self.path, "driving_log.csv")
        df = odo(csv_path, DataFrame, dshape='var * {center: string, left: string, right: string, steering: float64, throttle: float64, brake: float64, speed: float64}')

        if "timestamp" not in df:
            timestamp = (int)(time.time() * 1000)
            n = len(df)

            df["timestamp"] = np.arange(n) * 100 + timestamp

        df = normalize_dataframe(df)
        df["filename"] = df["filename"].str.replace("IMG/", "").str.strip()



# df.iloc[0].filename

        msk = np.random.rand(len(df)) < train_size

        train = df[msk]
        test = df[~msk]

        print("Moving Files")
        move_files(train['filename'].values, os.path.join(self.path, "IMG"), os.path.join(self.path, 'training-set'))
        move_files(test['filename'].values, os.path.join(self.path, "IMG"), os.path.join(self.path, 'test-set'))

        (_coconut_partial(odo, {0: train}, 2))(os.path.join(self.path, "training-set", "data.csv"))
        (_coconut_partial(odo, {0: test}, 2))(os.path.join(self.path, "test-set", "data.csv"))


        print("Removing folders")
        (shutil.rmtree)(os.path.join(self.path, "__MACOSX"))
        (shutil.rmtree)(os.path.join(self.path, "data"))
        (shutil.rmtree)(os.path.join(self.path, "IMG"))


def normalize_dataframe(df):
    import pandas as pd

    df_L = df.copy()
    df_C = df.copy()
    df_R = df.copy()

    df_L["camera"] = 0
    df_C["camera"] = 1
    df_R["camera"] = 2

    df_L["filename"] = df_L["left"]
    df_C["filename"] = df_C["center"]
    df_R["filename"] = df_R["right"]

    df_L = df_L.drop(["left", "center", "right"], axis=1)
    df_C = df_C.drop(["left", "center", "right"], axis=1)
    df_R = df_R.drop(["left", "center", "right"], axis=1)

    df = pd.concat([df_L, df_C, df_R])

    return df
