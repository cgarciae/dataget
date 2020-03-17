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


class free_spoken_digit(Dataset):
    @property
    def name(self):
        return "audio_free_spoken_digit"

    async def download(self):

        zip_path = self.path / "free-spoken-digit-dataset.zip"

        async with httpx.AsyncClient() as client:
            await utils.download_file(
                client,
                "https://github.com/Jakobovski/free-spoken-digit-dataset/archive/master.zip",
                zip_path,
            )

        utils.unzip(zip_path, self.path)

        files_path = self.path / "free-spoken-digit-dataset-master"

        for path in files_path.iterdir():
            if path.is_dir() and path != files_path / "recordings":
                shutil.rmtree(path)
            elif path.is_file():
                path.unlink()

    def load(self):
        recordings_path = self.path / "free-spoken-digit-dataset-master" / "recordings"

        file_paths = list(recordings_path.iterdir())
        file_paths = sorted(file_paths)

        df = pd.DataFrame(
            (
                dict(
                    audio_path=[str(path) for path in file_paths],
                    audio_name=[path.stem for path in file_paths],
                )
            )
        )

        df_new = (
            # print(
            df["audio_name"]
            .str.split("_")
            .apply([lambda x: int(x[0]), lambda x: x[1], lambda x: int(x[2])])
        )

        df_new.columns = [1, 2, 3]

        df[["label", "user", "repetition"]] = df_new

        df.drop(columns=["audio_name"], inplace=True)

        return df

