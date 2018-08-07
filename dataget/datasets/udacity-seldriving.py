import urllib
import zipfile
import os
import shutil
from dataget.utils import get_file, move_files
from dataget.api import register_dataset
from multiprocessing import Pool
from dataget.core import DataSet
import time
import pandas as pd


URL = "https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584f6edd_data/data.zip"

@register_dataset
class UdacitySelfdrivingSimulator(DataSet):

    def __init__(self, *args, **kwargs):
        self.normalize = kwargs.pop("normalize", True)

        super(UdacitySelfdrivingSimulator, self).__init__(*args, **kwargs)

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
                df.columns = [ "center", "left", "right", "steering", "throttle", "brake", "speed" ]
                

                if self.normalize:
                    df = normalize_dataframe(df)

                    filepath_base = df.filename.iloc[0]
                    filepath_base = filepath_base.split("/")[:-2]
                    filepath_base = os.sep.join(filepath_base)
                    filepath_base = os.path.join(filepath_base, "IMG") + os.sep

                    
                    df["filename"] = df.filename.str.replace(filepath_base, '').str.strip()
                    df["filepath"] = os.path.join(self.path, folder, "IMG") + os.sep + df.filename
                
                else:
                    filepath_base = df.center.iloc[0]
                    filepath_base = filepath_base.split("/")[:-2]
                    filepath_base = os.sep.join(filepath_base)
                    filepath_base = os.path.join(filepath_base, "IMG") + os.sep

                    
                    df["left"] = df.left.str.replace(filepath_base, '').str.strip()
                    df["left_filepath"] = os.path.join(self.path, folder, "IMG") + os.sep + df.left

                    df["center"] = df.center.str.replace(filepath_base, '').str.strip()
                    df["center_filepath"] = os.path.join(self.path, folder, "IMG") + os.sep + df.center
                    
                    df["right"] = df.right.str.replace(filepath_base, '').str.strip()
                    df["right_filepath"] = os.path.join(self.path, folder, "IMG") + os.sep + df.right

                
                df["folder"] = folder

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
