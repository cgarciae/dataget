import os

import aiofiles
import httpx
import idx2numpy
import pandas as pd
import asyncio

from dataget import utils
from dataget.dataset import Dataset


class fashion_mnist(Dataset):
    @property
    def name(self):
        return "image_fashion_mnist"

    async def download(self):

        base_url = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/"
        files = {
            "train-labels": base_url + "train-labels-idx1-ubyte.gz",
            "train-features": base_url + "train-images-idx3-ubyte.gz",
            "test-labels": base_url + "t10k-labels-idx1-ubyte.gz",
            "test-features": base_url + "t10k-images-idx3-ubyte.gz",
        }

        async with httpx.AsyncClient() as client:
            tasks = [
                self._download_file(client, url, name) for name, url in files.items()
            ]

            await asyncio.gather(*tasks)

    async def _download_file(self, client, url, name):
        gz_path = self.path / f"{name}.gz"
        idx_path = self.path / f"{name}.idx"

        await utils.download_file(client, url, gz_path)
        await utils.run_in_executor(lambda: utils.ungzip(gz_path, idx_path))

        gz_path.unlink()

    def load(self):

        with open(self.path / "train-features.idx", "rb") as f:
            X_train = idx2numpy.convert_from_file(f)

        with open(self.path / "train-labels.idx", "rb") as f:
            y_train = idx2numpy.convert_from_file(f)

        with open(self.path / "test-features.idx", "rb") as f:
            X_test = idx2numpy.convert_from_file(f)

        with open(self.path / "test-labels.idx", "rb") as f:
            y_test = idx2numpy.convert_from_file(f)

        return X_train, y_train, X_test, y_test
