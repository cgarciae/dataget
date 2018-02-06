from __future__ import print_function, absolute_import, unicode_literals, division
from dataget.dataset import ImageDataSet
from dataget.utils import get_file, maybe_mkdir
from dataget.api import register_dataset
import gzip
import os

TRAIN_FEATURES_URL = "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
TRAIN_LABELS_URL = "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"
TEST_FEATURES_URL = "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"
TEST_LABELS_URL = "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"

def ungzip(src_name, dest_name):
    print("extracting {}".format(dest_name))

    with gzip.open(src_name, 'rb') as infile:
        with open(dest_name, 'wb') as outfile:
            for line in infile:
                outfile.write(line)


def arrays_to_images(path, images, labels, dims, format, dataset):
    from PIL import Image

    last = -1
    n = len(labels)

    for i, (array_img, label) in enumerate(zip(images, labels)):

        label = str(label)
        class_path = maybe_mkdir(os.path.join(path, label)) 
        class_path = maybe_mkdir(os.path.join(path, label)) 

        with Image.fromarray(array_img) as im:
            im = im.resize(dims)
            im.save(
                os.path.join(
                    class_path,
                    "{}-{}.{}".format(dataset, i, format)
                ),
                quality=100
            )

        percent = int(float(i + 1) / n * 100)
        if percent % 10 == 0 and percent != last:
            print("{}%".format(percent))
            last = percent


@register_dataset
class Mnist(ImageDataSet):

    @property
    def _raw_extension(self):
        pass

    @property
    def help(self):
        return "" # information for the help command

    def reqs(self, **kwargs):
        return super(Mnist, self).reqs() + " " + "idx2numpy" # e.g. "numpy pandas pillow"

    def _download(self, **kwargs):
        get_file(TRAIN_FEATURES_URL, self.path, "train-features.gz")
        get_file(TRAIN_LABELS_URL, self.path, "train-labels.gz")
        get_file(TEST_FEATURES_URL, self.path, "test-features.gz")
        get_file(TEST_LABELS_URL, self.path, "test-labels.gz")

    def _extract(self, **kwargs):

        ungzip(
            os.path.join(self.path, "train-features.gz"),
            os.path.join(self.path, "train-features.idx")
        )

        ungzip(
            os.path.join(self.path, "train-labels.gz"),
            os.path.join(self.path, "train-labels.idx")
        )

        ungzip(
            os.path.join(self.path, "test-features.gz"),
            os.path.join(self.path, "test-features.idx")
        )

        ungzip(
            os.path.join(self.path, "test-labels.gz"),
            os.path.join(self.path, "test-labels.idx")
        )


    def _process(self, dims="28x28", format="jpg", **kwargs):
        from idx2numpy import convert_from_file

        dims = dims.split('x')
        dims = tuple(map(int, dims))

        print("Image dims: {}, format: {}".format(dims, format))

        print("processing training-set")
        arrays_to_images(
            path = self.path,
            images = convert_from_file(os.path.join(self.path, "train-features.idx")),
            labels = convert_from_file(os.path.join(self.path, "train-labels.idx")),
            dims = dims,
            format = format,
            dataset = "train",
        )

        print("processing test-set")
        arrays_to_images(
            path = self.path,
            images = convert_from_file(os.path.join(self.path, "test-features.idx")),
            labels = convert_from_file(os.path.join(self.path, "test-labels.idx")), 
            dims = dims,
            format = format,
            dataset = "test",
        )


    def _rm_raw(self, **kwargs):
        print("removing raw")
        os.remove(os.path.join(self.path, "train-features.idx")) 
        os.remove(os.path.join(self.path, "train-labels.idx")) 
        os.remove(os.path.join(self.path, "test-features.idx")) 
        os.remove(os.path.join(self.path, "test-labels.idx")) 
