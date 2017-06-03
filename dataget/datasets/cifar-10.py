from __future__ import print_function, absolute_import, unicode_literals, division

import os, sys, urllib, zipfile, shutil
from dataget.dataset import ImageDataSet
from dataget.utils import get_file
from dataget.api import register_dataset
import tarfile
import numpy as np


TRAINING_SET_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"

def unpickle(file):
    import cPickle
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo)
    return dict

@register_dataset
class Cifar10(ImageDataSet):

    def __init__(self, *args, **kwargs):
        super(Cifar10, self).__init__(*args, **kwargs)

        # self.path
        # self.training_set
        # self.training_set.path
        # self.training_set.make_dirs()
        # self.test_set
        # self.test_set.path
        # self.test_set.make_dirs()

    @property
    def _raw_extension(self):
        return "jpg"

    @property
    def help(self):
        return "" # information for the help command

    def reqs(self, **kwargs):
        return super(Cifar10, self).reqs() + "" # e.g. "numpy pandas pillow"


    def _download(self, **kwargs):
        get_file(TRAINING_SET_URL, self.path, "complete-set.tar.gz")



    def _extract(self, **kwargs):
        from PIL import Image
        # extract the data
        print("Extracting zip")

        with tarfile.open(os.path.join(self.path,"complete-set.tar.gz")) as zip_ref:
            zip_ref.extractall(self.path)

        dirdata = os.path.join(self.path,"cifar-10-batches-py")
        num_batches = 5 #5 training batches plus one test_batch
        SZ = 32
        for j in range(0 ,num_batches+1):
            if (j == 0):
                    dirname = os.path.join(self.path,"test-set")
                    x = unpickle(os.path.join(dirdata,"test_batch"))
            else:
                x = unpickle(os.path.join(dirdata,"data_batch_" + str(j)))
                dirname = os.path.join(self.path,"training-set")

            imgs = x["data"]
            labels = x["labels"]
            N = len(imgs)

            for i in range(N):
                mkdir = os.path.join(dirname,str(labels[i]))
                if not os.path.exists(mkdir):
                    os.mkdir(mkdir)
                rgbArray = np.zeros((SZ,SZ,3), 'uint8')
                rgbArray[..., 0] = imgs[i,0:SZ*SZ]. reshape(32,32)
                rgbArray[..., 1] = imgs[i,SZ*SZ:SZ*SZ*2].reshape(32,32)
                rgbArray[..., 2] = imgs[i,SZ*SZ*2:SZ*SZ*3+1].reshape(32,32)
                img = Image.fromarray(rgbArray)
                img.save(os.path.join(mkdir,str(i+(j-1)*N)+'.jpg') )

        shutil.rmtree(dirdata)
