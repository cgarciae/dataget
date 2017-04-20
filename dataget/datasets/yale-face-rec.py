from __future__ import print_function, absolute_import, unicode_literals, division
import os, sys, urllib, zipfile, shutil
from dataget.dataset import DataSet, SubSet
from dataget.utils import get_file

TRAINING_SET_URL = "http://vision.ucsd.edu/extyaleb/CroppedYaleBZip/CroppedYale.zip"

class YaleFaceRecSet(DataSet):

    def __init__(self, *args, **kwargs):
        super(YaleFaceRecSet, self).__init__(*args, **kwargs)

        # self.path
        # self.training_set
        # self.training_set.path
        # self.training_set.make_dirs()
        # self.test_set
        # self.test_set.path
        # self.test_set.make_dirs()


    @property
    def training_set_class(self):
        return TrainingSetMyDataSet

    @property
    def test_set_class(self):
        return TestSetMyDataSet

    @property
    def help(self):
        return "" # information for the help command

    def reqs(self, **kwargs):
        return "numpy pillow pandas" # e.g. "numpy pandas pillow"


    def _download(self, **kwargs):
        self.training_set.make_dirs()
        self.test_set.make_dirs()
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

                if file.endswith(".pgm"):

                    direct = file.split('/')

                    img = direct[-1].split('_')


                    mkdir = os.path.join(self.path, "training-set",str(int(img[0][-2::])) )
                    mkdir2 = os.path.join(self.path, "test-set",str(int(img[0][-2::])))

                    if not os.path.exists(mkdir):
                        os.mkdir(mkdir, 0755 );
                    if not os.path.exists(mkdir2):
                        os.mkdir(mkdir2, 0755 );
                    if not ("Ambient" in img[-1]):
                        if (i%5 == 0):
                            os.rename(file,mkdir2+'/'+direct[-1])
                        else:
                            os.rename(file,mkdir+'/'+direct[-1])
                    i+=1

        shutil.rmtree(os.path.join(self.path,"CroppedYale"))


    def _remove_compressed(self, **kwargs):
        os.remove(os.path.join(self.path,"MIT-CBCL-facerec-database.zip"))

    def _process(self, dims="128x128", format="jpg", **kwargs):
        from PIL import Image

        dims = dims.split('x')
        dims = tuple(map(int, dims))

        print("Image dims: {}, Image format: {}".format(dims, format))

        CLASS = None

        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = os.path.join(root, file)

                if file.endswith(".pgm"):

                    new_file = file.replace(".pgm", ".{}".format(format))

                    with Image.open(file) as im :
                        im = im.resize(dims)
                        im.save(new_file, quality=100)

                    dirs = file.split("/")
                    _class = dirs[-2]
                    current_set =  dirs[-3]

                    if _class != CLASS:
                        CLASS = _class
                        print("formating {} {}".format(current_set, _class))

    def _remove_raw(self, **kwargs):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = os.path.join(root, file)
                if file.endswith(".pgm"):
                    os.remove(file)


class MySetBase(SubSet):

    #self.path
    #self.make_dirs()

    def dataframe(self):
        # code
        return df


    def arrays(self):
        # code
        return features, labels


    def random_batch_dataframe_generator(self, batch_size):
        # code
        yield df


    def random_batch_arrays_generator(self, batch_size):
        # code
        yield features, labels


class TrainingSetMyDataSet(MySetBase):


       def __init__(self, dataset, **kwargs):
           super(TrainingSetMyDataSet, self).__init__(dataset, "training-set", **kwargs)
           #self.path
           #self.make_dirs()


class TestSetMyDataSet(MySetBase):

      def __init__(self, dataset, **kwargs):
          super(TestSetMyDataSet, self).__init__(dataset, "test-set", **kwargs)
          #self.path
          #self.make_dirs()
