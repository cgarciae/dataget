import asyncio
import os
import pickle
import shutil
import sys
import tarfile

import aiofiles
import httpx
import idx2numpy
import numpy as np
import pandas as pd

from dataget import utils
from dataget.dataset import Dataset


class udacity_simulator(Dataset):
    @property
    def name(self):
        return "image_udacity_simulator"

    async def download(self):

        zip_path = self.path / "data.zip"

        async with httpx.AsyncClient() as client:
            await utils.download_file(
                client,
                "https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584f6edd_data/data.zip",
                zip_path,
            )

        utils.unzip(zip_path, self.path)

        zip_path.unlink()
        shutil.rmtree(self.path / "__MACOSX")

    def load(self):
        images_path = str(self.path / "data" / "IMG")

        df = pd.read_csv(self.path / "data" / "driving_log.csv")

        df["center"] = (
            images_path + os.sep + df["center"].str.strip().str.replace("IMG/", "")
        )
        df["left"] = (
            images_path + os.sep + df["left"].str.strip().str.replace("IMG/", "")
        )
        df["right"] = (
            images_path + os.sep + df["right"].str.strip().str.replace("IMG/", "")
        )

        return df


class cifar100(Dataset):
    @property
    def name(self):
        return "image_cifar100"

    async def download(self):

        gz_path = self.path / "cifar-10-python.tar.gz"

        async with httpx.AsyncClient() as client:
            await utils.download_file(
                client,
                "https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz",
                gz_path,
            )

        with tarfile.open(gz_path) as zip_ref:
            zip_ref.extractall(self.path)

        gz_path.unlink()

    def load(self):
        path = self.path / "cifar-100-python"

        fpath = path / "train"
        X_train, y_train = load_batch(fpath, label_key="fine_labels")

        fpath = path / "test"
        X_test, y_test = load_batch(fpath, label_key="fine_labels")

        y_train = np.reshape(y_train, (len(y_train), 1))
        y_test = np.reshape(y_test, (len(y_test), 1))

        return X_train, y_train, X_test, y_test


def load_batch(fpath, label_key="labels"):
    """Internal utility for parsing CIFAR data.
  Arguments:
      fpath: path the file to parse.
      label_key: key for label data in the retrieve
          dictionary.
  Returns:
      A tuple `(data, labels)`.
  """
    with open(fpath, "rb") as f:
        if sys.version_info < (3,):
            d = pickle.load(f)
        else:
            d = pickle.load(f, encoding="bytes")
            # decode utf8
            d_decoded = {}
            for k, v in d.items():
                d_decoded[k.decode("utf8")] = v
            d = d_decoded
    data = d["data"]
    labels = d[label_key]

    data = data.reshape(data.shape[0], 3, 32, 32)
    data = data.transpose(0, 2, 3, 1)
    return data, labels
