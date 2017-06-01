from __future__ import print_function, absolute_import, unicode_literals, division
import os, sys, urllib, stat, zipfile, time

from dataget.utils import get_file
from dataget.api import register_dataset
from dataget.dataset import ImageDataSet

TRAINING_SET_URL = "http://cbcl.mit.edu/software-datasets/heisele/download/download.html"


@register_dataset
class MitFaceRec(ImageDataSet):

    def __init__(self, *args, **kwargs):
        super(MitFaceRec, self).__init__(*args, **kwargs)

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
        return super(MitFaceRec, self).reqs() + " selenium" # e.g. "numpy pandas pillow"


    def _download(self, **kwargs):
        from selenium import webdriver
        # download the data, propably a compressed format
        self.training_set.make_dirs()
        self.test_set.make_dirs()

        #check OS version: 'linux2' ,'win32' or 'darwin'(MAC)
        version = sys.platform
        extension = ""
        if version == 'linux2':
            if sys.maxsize > 2**32: #it is then 64 bits
                webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip'
            else:
                webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux32.zip'
        elif version == 'win32':
            extension = ".exe"
            webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_win32.zip'
        elif version == 'darwin':
            webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_mac64.zip'
        else:
            raise ValueError("No supported OS")

        #Download now driver
        get_file(webdriver_url,self.path,"chromedriver.zip")

        #Extract it, chmod to +x and delete zip
        with zipfile.ZipFile(os.path.join(self.path,"chromedriver.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.path)

        chromename = os.path.join(self.path,"chromedriver") + extension
        st = os.stat(chromename)
        os.chmod(chromename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : self.path}
        chromeOptions.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(executable_path=chromename, chrome_options=chromeOptions)

        #Donwload
        print("Downloading dataset...\n (... it may open a chrome window, please dont close it ...)")
        TRAINING_SET_URL = "http://cbcl.mit.edu/software-datasets/heisele/download/download.html"
        driver.get(TRAINING_SET_URL)
        driver.find_element_by_link_text("download now").click();

        #Wait to download to complete
        file_path = self.path + "/MIT-CBCL-facerec-database.zip"
        value = 0
        print("0%")
        while not os.path.exists(file_path):
            if os.path.exists(file_path+".crdownload"):
                statinfo = os.stat(file_path+".crdownload")
                downloaded = int (statinfo.st_size/121643276.0*100)
                if (downloaded%5 == 0 and value != downloaded):
                    value = downloaded
                    print("{}%".format(downloaded))
            time.sleep(0.5)

        print("DONE")
        driver.quit()
        os.remove(chromename)
        os.remove(os.path.join(self.path,"chromedriver.zip"))


    def _process(self, dims="128x128", format="jpg", **kwargs):
        super(MitFaceRec, self)._process(dims=dims, format=format, **kwargs)

    def _extract(self, **kwargs):
        # extract the data
        print("Extracting zip")
        with zipfile.ZipFile(os.path.join(self.path,"MIT-CBCL-facerec-database.zip"), 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith('test/'):
                    zip_ref.extract(file, self.path)

        for root, dirs, files in os.walk(os.path.join(self.path,"test")):
            files.sort()
            i = 0
            for file in files:
                file = os.path.join(root, file)

                if file.endswith(self.raw_extension):

                    direct = file.split(os.sep)

                    clase = direct[-1].split('_')

                    mkdir = os.path.join(self.path, "training-set",str(int(clase[0])) )
                    if (i%10 == 0):
                        mkdir = os.path.join(self.path, "test-set",str(int(clase[0])) )
                    if not os.path.exists(mkdir):
                        os.mkdir(mkdir)
                    os.rename(file,os.path.join(mkdir,direct[-1]))
                    i+=1

        os.rmdir(os.path.join(self.path,"test"))
