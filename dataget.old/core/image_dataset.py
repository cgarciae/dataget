from __future__ import print_function, absolute_import, unicode_literals, division
from abc import abstractproperty
from .dataset import DataSet
import os, random
from dataget.utils import OS_SPLITTER
from dataget.utils import read_pillow_image
import pandas as pd

#####



####

class ImageDataSet(DataSet):

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

        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = os.path.join(root, file)

                if file.endswith(self.raw_extension):

                    new_file = file.replace(self.raw_extension, ".{}".format(format))

                    with Image.open(file) as im:
                        im = im.resize(dims)
                        im.save(new_file, quality=100)

                    dirs = file.split(OS_SPLITTER)
                    _class = dirs[-2]
                    _set = dirs[-3]

                    if _class != CLASS:
                        CLASS = _class
                        print("formating {} {}".format(_set, _class))

                elif file.endswith(".csv"):

                    df = pd.read_csv(file)
                    df['filename'] =  df['filename'].str.replace(self.raw_extension, "." + format)

                    print("formatting {}".format(file))

                    self.process_dataframe(df, dims=dims, format=format, **kwargs)

                    df.to_csv(file, index=False)

    def _rm_raw(self, **kwargs):
        self.remove_all_file_with_extension(self._raw_extension)

    @property
    def n_classes(self):
        return len(os.listdir(self.training_set.path))

    def _dict_generator(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if root != self.path:
                    class_id = root.split(OS_SPLITTER)[-1]
                    try:
                        class_id = int(class_id)
                    except:
                        pass

                    yield dict(
                        filename = os.path.join(root, file),
                        class_id = class_id
                    )


    def get_df(self):
        return pd.DataFrame(self._dict_generator())