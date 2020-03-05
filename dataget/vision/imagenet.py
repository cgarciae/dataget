import os

import aiofiles
import httpx
import idx2numpy
import pandas as pd
import asyncio

from dataget import utils
from dataget.dataset import Dataset


class imagenet(Dataset):
    @property
    def name(self):
        return "vision_imagenet"

    async def download(self, **kwargs):

        subprocess.check_call(
            f"kaggle datasets download -p {self.path} --unzip {self.kaggle_dataset}",
            shell=True,
        )

        async with httpx.AsyncClient() as client:
            tasks = [
                self._download_file(client, TRAIN_FEATURES_URL, "train-features"),
                self._download_file(client, TRAIN_LABELS_URL, "train-labels"),
                self._download_file(client, TEST_FEATURES_URL, "test-features"),
                self._download_file(client, TEST_LABELS_URL, "test-labels"),
            ]

            await asyncio.gather(*tasks)

    async def _download_file(self, client, url, name):
        gz_path = self.path / f"{name}.gz"
        idx_path = self.path / f"{name}.idx"

        await utils.download_file(client, url, gz_path)
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: utils.ungzip(gz_path, idx_path)
        )

        gz_path.unlink()

    def load(self, **kwargs):

        with open(self.path / "train-features.idx", "rb") as f:
            X_train = idx2numpy.convert_from_file(f)

        with open(self.path / "train-labels.idx", "rb") as f:
            y_train = idx2numpy.convert_from_file(f)

        with open(self.path / "test-features.idx", "rb") as f:
            X_test = idx2numpy.convert_from_file(f)

        with open(self.path / "test-labels.idx", "rb") as f:
            y_test = idx2numpy.convert_from_file(f)

        return X_train, y_train, X_test, y_test
