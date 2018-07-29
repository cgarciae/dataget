import urllib
import zipfile
import os
import shutil
from dataget.utils import get_file, move_files
from dataget.api import register_dataset
from multiprocessing import Pool
from dataget.dataset import ImageNavigationDataSet
import time
import pandas as pd


URL = "https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584f6edd_data/data.zip"

@register_dataset
class UdacitySelfdrivingSimulator(ImageNavigationDataSet):

    @property
    def features(self):
        return ["image", "speed", "camera"]

    @property
    def labels(self):
        return ["steering", "throttle", "brake", "original_steering"]

    @property
    def _raw_extension(self):
        return "jpg"

    @property
    def help(self):
        return "TODO"

    def reqs(self, **kwargs):
        return super(UdacitySelfdrivingSimulator, self).reqs() + ""

    def _download(self, **kwargs):
        get_file(URL, self.path, "dataset.zip")

    def _extract(self, train_size = 0.8, **kwargs):

        print("Extracting zip")
        with zipfile.ZipFile(os.path.join(self.path, "dataset.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.path)

        shutil.rmtree(os.path.join(self.path, "__MACOSX"))

        # os.path.join(self.path, "data", "IMG")
        # shutil.move(?, self.path)
        # os.path.join(self.path, "data", "driving_log.csv")
        # shutil.move(?, self.path)


        # print("Loading Data")
        # csv_path = os.path.join(self.path, "driving_log.csv")
        # df = pd.read_csv(csv_path)

        # if "timestamp" not in df:
        #     timestamp = time.time() * 1000 |> int
        #     n = len(df)

        #     df["timestamp"] = np.arange(n) * 100 + timestamp

        # df = normalize_dataframe(df)
        # df["filename"] = df["filename"].str.replace("IMG/", "").str.strip()



        # # df.iloc[0].filename

        # msk = np.random.rand(len(df)) < train_size

        # train = df[msk]
        # test = df[~msk]

        # print("Moving Files")
        # move_files(train['filename'].values, os.path.join(self.path, "IMG"), os.path.join(self.path, 'training-set'))
        # move_files(test['filename'].values, os.path.join(self.path, "IMG"), os.path.join(self.path, 'test-set'))

        # os.path.join(self.path, "training-set", "data.csv") |> train.to_csv$(?, index = False)
        # os.path.join(self.path, "test-set", "data.csv") |> test.to_csv$(?, index = False)


        # print("Removing folders")
        # os.path.join(self.path, "__MACOSX")
        # os.path.join(self.path, "data") |> shutil.rmtree
        # os.path.join(self.path, "IMG") |> shutil.rmtree

    def _process(self, **kwargs):
        print("This class wont process the data... :|")

    def _rm_raw(self, **kwargs):
        print("This class wont remove raw... :|")

    def get_df(self):
        
        dfs = []

        for folder in os.listdir(self.path):
            folder_path = os.path.join(self.path, folder)

            if os.path.isdir(folder_path):

                csv_path = os.path.join(folder_path, "driving_log.csv")

                df = pd.read_csv(csv_path)
                df = normalize_dataframe(df)

                filepath_base = df.filename.iloc[0]
                filepath_base = filepath_base.split("/")[:-2]
                filepath_base = "/".join(filepath_base)

                print("BASEPATH", filepath_base)

                df["filename"] = df.filename.str.replace(filepath_base, '')
                df["filename"] = self.path + "/" + folder + "/" + df.filename.str.lstrip()
            
                dfs.append(df)
    
        return pd.concat(dfs)


def normalize_dataframe(df):
    
    df_L = df.copy()
    df_C = df.copy()
    df_R = df.copy()

    df_L["camera"] = 0
    df_C["camera"] = 1
    df_R["camera"] = 2

    df_L["filename"] = df_L["left"]
    df_C["filename"] = df_C["center"]
    df_R["filename"] = df_R["right"]

    df_L = df_L.drop(["left", "center", "right"], axis = 1)
    df_C = df_C.drop(["left", "center", "right"], axis = 1)
    df_R = df_R.drop(["left", "center", "right"], axis = 1)

    df = pd.concat([df_L, df_C, df_R])

    return df
