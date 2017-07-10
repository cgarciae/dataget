#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf7c55c36

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

from abc import abstractmethod
from .image_dataset import ImageDataSet
from .image_dataset import ImageSubSet
import os
from dataget.utils import OS_SPLITTER


class ImageDataSetWithMetadata(ImageDataSet):

    @abstractmethod
    def process_dataframe(self, dataframe, **kwargs):
        pass


    @property
    def training_set_class(self):
        return ImageSubSetWithMetadata

    @property
    def test_set_class(self):
        return ImageSubSetWithMetadata



class ImageSubSetWithMetadata(ImageSubSet):

    def _dataframe_generator(self):
        import pandas as pd

        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = os.path.join(root, file)

                if file.endswith(".csv"):
                    df = pd.read_csv(file)
                    df["filename"] = root + OS_SPLITTER + df["filename"]

                    yield df

    def _load_dataframe(self):
        if self._dataframe is None:
            import pandas as pd
            self._dataframe = pd.concat(self._dataframe_generator())
