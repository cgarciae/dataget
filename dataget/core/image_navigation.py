from __future__ import print_function, absolute_import, unicode_literals, division
from abc import abstractproperty, abstractmethod
from .dataset import DataSet
import os, random
import numpy as np
import pandas as pd


class ImageNavigationDataSet(DataSet):

    @abstractproperty
    def _raw_extension(self):
        pass

    @property
    def raw_extension(self):
        return ".{}".format(self._raw_extension)

    def reqs(self, **kwargs):
        return "pillow pandas numpy"


    def _process(self, dims="32x32", format="jpg", **kwargs):
        from PIL import Image

        dims = dims.split('x')
        dims = tuple(map(int, dims))

        print("Image dims: {}, Image format: {}".format(dims, format))


        CLASS = None
        dataset_path = self.path

        for root, dirs, files in os.walk(dataset_path):
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
                    df['filename'] =  df['filename'].str.replace(self.raw_extension, "." + format)

                    print("formatting {}".format(file))

                    df.to_csv(file, index=False)

    def _rm_raw(self, **kwargs):
        self.remove_all_file_with_extension(self._raw_extension)


    def get_df(self):
        
        csv_path = os.path.join(self.path, "data.csv")
        df = pd.read_csv(csv_path)

        df["filename"] = self.path + os.sep + df["filename"]

        # set fields
        return df