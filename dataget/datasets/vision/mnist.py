import os

import aiofiles
import httpx
import idx2numpy
import pandas as pd
import asyncio

from dataget import utils
from dataget.api import register_dataset
from dataget.dataset import Dataset

TRAIN_FEATURES_URL = "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
TRAIN_LABELS_URL = "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"
TEST_FEATURES_URL = "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"
TEST_LABELS_URL = "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"


@register_dataset
class Mnist(Dataset):
    async def download(self, **kwargs):

        ###############################################################
        # download data
        ###############################################################

        async with httpx.AsyncClient() as client:
            tasks = [
                self._download_file(client, TRAIN_FEATURES_URL, "train-features"),
                self._download_file(client, TRAIN_LABELS_URL, "train-labels"),
                self._download_file(client, TEST_FEATURES_URL, "test-features"),
                self._download_file(client, TEST_LABELS_URL, "test-labels"),
            ]

            tasks = [asyncio.create_task(task) for task in tasks]

            await asyncio.gather(*tasks)

        ###############################################################
        # transform data
        ###############################################################

        with open(self.path / "train-features.idx", "rb") as f:
            X_train = idx2numpy.convert_from_file(f)

        with open(self.path / "train-labels.idx", "rb") as f:
            y_train = idx2numpy.convert_from_file(f)

        with open(self.path / "test-features.idx", "rb") as f:
            X_test = idx2numpy.convert_from_file(f)

        with open(self.path / "test-labels.idx", "rb") as f:
            y_test = idx2numpy.convert_from_file(f)

        df_train = pd.concat(
            [
                pd.DataFrame(y_train[:, None], columns=["label"]),
                pd.DataFrame(
                    X_train.reshape(X_train.shape[0], -1),
                    columns=[str(i) for i in range(28 * 28)],
                ),
            ],
            axis=1,
        ).reset_index(drop=True)

        df_test = pd.concat(
            [
                pd.DataFrame(y_test[:, None], columns=["label"]),
                pd.DataFrame(
                    X_test.reshape(X_test.shape[0], -1),
                    columns=[str(i) for i in range(28 * 28)],
                ),
            ],
            axis=1,
        ).reset_index(drop=True)

        ###############################################################
        # serialize data
        ###############################################################

        df_train.to_feather(self.path / "train.feather")
        df_test.to_feather(self.path / "test.feather")

        ###############################################################
        # cleanup
        ###############################################################

        (self.path / "train-features.idx").unlink()
        (self.path / "train-labels.idx").unlink()
        (self.path / "test-features.idx").unlink()
        (self.path / "test-labels.idx").unlink()

    async def _download_file(self, client, url, name):
        gz_path = self.path / f"{name}.gz"
        idx_path = self.path / f"{name}.idx"

        await utils.download_file(client, url, gz_path)
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: utils.ungzip(gz_path, idx_path)
        )

        gz_path.unlink()

    def is_valid(self, **kwargs):
        return (self.path / "train.feather").exists() and (
            self.path / "test.feather"
        ).exists()

    def load_data(self, extras, **kwargs):

        df_train = pd.read_feather("train.feather")
        df_test = pd.read_feather("test.feather")

        outputs = (df_train, df_test)

        if extras:

            extras = dict(
                X_train=df_train[df_train.columns[1:]].to_numpy().reshape(-1, 28, 28),
                y_train=df_train[df_train.columns[0]].to_numpy(),
                X_test=df_test[df_test.columns[1:]].to_numpy().reshape(-1, 28, 28),
                y_test=df_test[df_test.columns[0]].to_numpy(),
            )

            outputs += (extras,)

        return outputs


if __name__ == "__main__":

    df_train, df_test, extras = Mnist("data").get(extras=True)

    X_train = extras["X_train"]
    y_train = extras["y_train"]
    X_test = extras["X_test"]
    y_test = extras["y_test"]

    print(df_train.shape)
    print(df_test.shape)
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)
