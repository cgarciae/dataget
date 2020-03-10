import asyncio
import os
import subprocess

import aiofiles
import httpx
import idx2numpy
import pandas as pd

from dataget import utils
from dataget.dataset import Dataset


class imagenet(Dataset):
    @property
    def name(self):
        return "image_imagenet"

    def download(self):

        subprocess.check_call(
            f"kaggle competitions download -p {self.path} imagenet-object-localization-challenge",
            shell=True,
        )

        zip_path = self.path / "imagenet-object-localization-challenge.zip"

        print(f"Extracting {zip_path}, this will take a while...")
        utils.unzip(zip_path, self.path)
        zip_path.unlink()

        gz_path = self.path / "imagenet_object_localization_patched2019.tar.gz"

        print(f"Extracting {gz_path}, this will take a while...")
        utils.untar(src_path=gz_path, dst_path=self.path, fast=True)
        gz_path.unlink()

    def load(self):

        with open(self.path / "LOC_synset_mapping.txt") as f:
            label_map = {}
            for line in f.readlines():
                splits = line[:-1].split(" ")
                label_map[splits[0]] = " ".join(splits[1:])

        df_train = self.load_train()
        df_val = self.load_val()
        df_test = self.load_test()

        df_train["label_name"] = df_train["label"].map(label_map)
        df_val["label_name"] = df_val["label"].map(label_map)

        return df_train, df_val, df_test

    def load_train(self):
        df = pd.read_csv(self.path / f"LOC_train_solution.csv")

        df["wnid"] = df["ImageId"].str.split("_").map(lambda x: x[0])

        df["image_path"] = (
            str(self.path / "ILSVRC" / "Data" / "CLS-LOC" / "train")
            + os.sep
            + df["wnid"]
            + os.sep
            + df["ImageId"]
            + ".JPEG"
        )

        df["annotations_path"] = (
            str(self.path / "ILSVRC" / "Annotations" / "CLS-LOC" / "train")
            + os.sep
            + df["wnid"]
            + os.sep
            + df["ImageId"]
            + ".xml"
        )

        labels_list = df["PredictionString"].str.split(" ")
        df["label"] = labels_list.map(lambda x: x[0])
        df["xmin"] = labels_list.map(lambda x: int(x[1]))
        df["ymin"] = labels_list.map(lambda x: int(x[2]))
        df["xmax"] = labels_list.map(lambda x: int(x[3]))
        df["ymax"] = labels_list.map(lambda x: int(x[4]))

        return df

    def load_val(self):
        df = pd.read_csv(self.path / f"LOC_val_solution.csv")

        df["image_path"] = (
            str(self.path / "ILSVRC" / "Data" / "CLS-LOC" / "val")
            + os.sep
            + df["ImageId"]
            + ".JPEG"
        )

        df["annotations_path"] = (
            str(self.path / "ILSVRC" / "Annotations" / "CLS-LOC" / "val")
            + os.sep
            + df["ImageId"]
            + ".xml"
        )

        labels_list = df["PredictionString"].str.split(" ")
        df["label"] = labels_list.map(lambda x: x[0])
        df["xmin"] = labels_list.map(lambda x: int(x[1]))
        df["ymin"] = labels_list.map(lambda x: int(x[2]))
        df["xmax"] = labels_list.map(lambda x: int(x[3]))
        df["ymax"] = labels_list.map(lambda x: int(x[4]))

        return df

    def load_test(self):
        df = pd.read_csv(self.path / f"LOC_sample_submission.csv")

        df["image_path"] = (
            str(self.path / "ILSVRC" / "Data" / "CLS-LOC" / "test")
            + os.sep
            + df["ImageId"]
            + ".JPEG"
        )

        df.drop(columns=["PredictionString"], inplace=True)

        return df
