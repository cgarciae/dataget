#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xeab03c04

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

from abc import abstractproperty
from abc import abstractmethod
from .dataset import DataSet
from .dataset import SubSet
import os
import random
from dataget.utils import read_pillow_image

class ImageNavigationDataSet(DataSet):

    @abstractproperty
    def features(self):
        pass

    @abstractproperty
    def labels(self):
        pass

    @abstractproperty
    def _raw_extension(self):
        pass

    @property
    def raw_extension(self):
        return ".{}".format(self._raw_extension)

    @property
    def training_set_class(self):
        return ImageNavigationSubSet

    @property
    def test_set_class(self):
        return ImageNavigationSubSet


    def reqs(self, **kwargs):
        return "pillow pandas numpy"

    def _process(self, dims="32x32", format="jpg", **kwargs):
        from PIL import Image

        dims = dims.split('x')
        dims = tuple(map(int, dims))

        print("Image dims: {}, Image format: {}".format(dims, format))

        CLASS = None

        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = os.path.join(root, file)

                if file.endswith(self.raw_extension):

                    new_file = file.replace(self.raw_extension, ".{}".format(format))

                    with Image.open(file) as im:
                        im = im.resize(dims)
                        im.save(new_file, quality=100)

                elif file.endswith(".csv"):
                    import pandas as pd

                    df = pd.read_csv(file)
                    df['filename'] = df['filename'].str.replace(self.raw_extension, "." + format)

                    print("formatting {}".format(file))

                    self.process_dataframe(df, dims=dims, format=format, **kwargs)

                    df.to_csv(file, index=False)

    def _rm_raw(self, **kwargs):
        self.remove_all_file_with_extension(self._raw_extension)




class ImageNavigationSubSet(SubSet):

    def __init__(self, *args, **kwargs):
        super(ImageNavigationSubSet, self).__init__(*args, **kwargs)
        self._dataframe = None
        self._features = None
        self._labels = None


    def process_dataframe(self, df, **kwargs):
        return df


    def _load_dataframe(self):
        if self._dataframe is None:
            import pandas as pd
            from odo import odo

            df = (_coconut_partial(odo, {1: pd.DataFrame}, 2))(os.path.join(self.path, "data.csv"))
            df["filename"] = self.path + os.sep + df["filename"]

            self._dataframe = df



    def pure_dataframe(self):

        self._load_dataframe()

        return self._dataframe


    def set_dataframe(self, dataframe):

        self._dataframe = dataframe

        return self

    def dataframe(self):
        import numpy as np
        from PIL import Image

        self._load_dataframe()

        if not "image" in self._dataframe:
            self._dataframe["image"] = (self._dataframe.filename.apply)(read_pillow_image(Image, np))

        return self._dataframe


    def arrays(self):
        import numpy as np

        if self._features is None or self._labels is None:
            dataframe = self.dataframe()

            self._features = dict(((name), (np.stack(dataframe[name].as_matrix()))) for name in self.dataset.features)
            self._labels = dict(((name), (np.stack(dataframe[name].as_matrix()))) for name in self.dataset.labels)

        return self._features, self._labels


    def random_batch_dataframe_generator(self, batch_size):
        import numpy as np
        from PIL import Image

        self._load_dataframe()

        while True:
            batch = self._dataframe.sample(batch_size)

            if not "image" in batch:
                batch["image"] = (batch.filename.apply)(read_pillow_image(Image, np))

            yield batch


    def random_batch_arrays_generator(self, batch_size):
        import numpy as np

        for data in self.random_batch_dataframe_generator(batch_size):

            features = dict(((name), (np.stack(data[name].as_matrix()))) for name in self.dataset.features)
            labels = dict(((name), (np.stack(data[name].as_matrix()))) for name in self.dataset.labels)

            yield features, labels
