from __future__ import print_function, absolute_import, unicode_literals, division

import os, sys, urllib, zipfile, shutil
from dataget.dataset import ImageDataSet
from dataget.utils import get_file
from dataget.api import register_dataset

TRAINING_SET_URL = "http://vision.ucsd.edu/extyaleb/CroppedYaleBZip/CroppedYale.zip"

@register_dataset
class YaleFaceRec(ImageDataSet):

    def __init__(self, *args, **kwargs):
        super(YaleFaceRec, self).__init__(*args, **kwargs)

        # self.path
        # self.training_set
        # self.training_set.path
        # self.training_set.make_dirs()
        # self.test_set
        # self.test_set.path
        # self.test_set.make_dirs()

    @property
    def _raw_extension(self):
        return "pgm"

    @property
    def help(self):
        return "" # information for the help command

    def reqs(self, **kwargs):
        return super(MitFaceRec, self).reqs() + "" # e.g. "numpy pandas pillow"


    def _download(self, **kwargs):
        get_file(TRAINING_SET_URL, self.path, "complete-set.zip")



    def _extract(self, **kwargs):
        # extract the data
        print("Extracting zip")
        with zipfile.ZipFile(os.path.join(self.path,"complete-set.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.path)

        for root, dirs, files in os.walk(os.path.join(self.path,"CroppedYale")):
            files.sort()
            i = 0
            for file in files:
                file = os.path.join(root, file)

                if file.endswith(self.raw_extension):

                    direct = file.split(os.sep)

                    img = direct[-1].split('_')


                    mkdir = os.path.join(self.path, "training-set",str(int(img[0][-2::])) )
                    mkdir2 = os.path.join(self.path, "test-set",str(int(img[0][-2::])))

                    if not os.path.exists(mkdir):
                        os.mkdir(mkdir)
                    if not os.path.exists(mkdir2):
                        os.mkdir(mkdir2)
                    if not ("Ambient" in img[-1]):
                        if (i%5 == 0):
                            os.rename(file,os.path.join(mkdir2,direct[-1]))
                        else:
                            os.rename(file,os.path.join(mkdir,direct[-1]))
                    i+=1

        shutil.rmtree(os.path.join(self.path,"CroppedYale"))
