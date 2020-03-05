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
        return "vision_imagenet"

    def download(self, **kwargs):

        subprocess.check_call(
            f"kaggle competitions download -p {self.path} imagenet-object-localization-challenge",
            shell=True,
        )

        zip_path = self.path / "imagenet-object-localization-challenge.zip"

        utils.ungzip(zip_path, self.path)
        zip_path.unlink()

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
