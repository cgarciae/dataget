from __future__ import print_function, absolute_import, unicode_literals, division
from abc import abstractmethod
from .image_dataset import ImageDataSet, ImageSubSet
import os
from dataget.utils import OS_SPLITTER


class ImageDataSetWithMetadata(ImageDataSet):

    def process_dataframe(self, dataframe, **kwargs):
        return dataframe

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
