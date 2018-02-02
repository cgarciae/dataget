from __future__ import print_function, absolute_import, unicode_literals, division
from abc import abstractproperty
from .dataset import DataSet, SubSet
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

    @property
    def subset_class(self):
        return ImageSubSet


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
                    import pandas as pd

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


    def _load_dataframe(self):
        return pd.DataFrame(self._dict_generator())



class ImageSubSet(SubSet):

    def __init__(self, *args, **kwargs):
        super(ImageSubSet, self).__init__(*args, **kwargs)
        self._features = None
        self._labels = None

    def dataframe(self):
        import numpy as np
        from PIL import Image

        self._load_dataframe()

        if not "image" in self._dataframe:
            self._dataframe["image"] = self._dataframe.filename.apply(read_pillow_image(Image, np))

        return self._dataframe


    def arrays(self):
        import numpy as np

        if self._features is None or self._labels is None:
            dataframe = self.dataframe()

            self._features = np.stack(dataframe.image.as_matrix())
            self._labels = np.stack(dataframe.class_id.as_matrix())

        return self._features, self._labels


    def random_batch_dataframe_generator(self, batch_size):
        import numpy as np
        from PIL import Image

        self._load_dataframe()

        while True:
            batch = self._dataframe.sample(batch_size)

            if not "image" in batch:
                batch["image"] = batch.filename.apply(read_pillow_image(Image, np)) 

            yield batch


    def random_batch_arrays_generator(self, batch_size):
        import numpy as np

        for data in self.random_batch_dataframe_generator(batch_size):
            features = np.stack(data.image.as_matrix())
            labels = np.stack(data.class_id.as_matrix())

            yield features, labels


    def class_sample(self, class_id, n_samples = 10):
        import numpy as np
        from PIL import Image

        if class_id >= self.dataset.n_classes or class_id < 0:
            raise Exception("Not a valid class. Classes go from 0 to N-1")
        self._load_dataframe()

        df = self._dataframe

        df = df[df.class_id==class_id]
        df = df.sample(n_samples)

        df["image"] = df.filename.apply(read_pillow_image(Image, np))

        return np.stack(df.image.as_matrix())
