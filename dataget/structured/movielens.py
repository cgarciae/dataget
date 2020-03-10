import asyncio
import math

import httpx
import numpy as np
import pandas as pd

from dataget import utils
from dataget.dataset import Dataset


class MovieLensBase(Dataset):
    @property
    def name(self):
        size = self.size.split("-")[1:]
        size = "_".join(size)
        return f"structured_movielens_{size}"

    async def download(self):
        zip_path = self.path / f"{self.size}.zip"

        async with httpx.AsyncClient() as client:
            await utils.download_file(
                client,
                f"http://files.grouplens.org/datasets/movielens/{self.size}.zip",
                zip_path,
            )

        utils.unzip(zip_path, self.path)
        zip_path.unlink()

    def load(self):
        output = (
            pd.read_csv(self.path / self.size / "ratings.csv"),
            pd.read_csv(self.path / self.size / "movies.csv"),
            pd.read_csv(self.path / self.size / "tags.csv"),
            pd.read_csv(self.path / self.size / "links.csv"),
        )

        if (self.path / self.size / "genome-scores.csv").exists():
            output += (
                pd.read_csv(self.path / self.size / "genome-scores.csv"),
                pd.read_csv(self.path / self.size / "genome-tags.csv"),
            )

        return output


class movielens_25m(MovieLensBase):
    @property
    def size(self):
        return "ml-25m"


class movielens_20m(MovieLensBase):
    @property
    def size(self):
        return "ml-20m"


class movielens_latest(MovieLensBase):
    @property
    def size(self):
        return "ml-latest"


class movielens_latest_small(MovieLensBase):
    @property
    def size(self):
        return "ml-latest-small"


class movielens_synthetic_1b(Dataset):
    @property
    def name(self):
        return f"structured_movielens_synthetic_1b"

    async def download(self):
        tar_path = self.path / "ml-20mx16x32.tar"

        async with httpx.AsyncClient() as client:
            await utils.download_file(
                client,
                f"http://files.grouplens.org/datasets/movielens/ml-20mx16x32.tar",
                tar_path,
            )

        utils.untar(tar_path, self.path)
        tar_path.unlink()

    def load(self, batch_size=None):
        if batch_size:
            return BatchedRatingsIterator(
                self.path / "ml-20mx16x32", batch_size=batch_size, total=1226159268
            )
        else:
            return RatingsIterable(self.path / "ml-20mx16x32")


class RatingsIterable:
    def __init__(self, path):
        self.file_paths = list(path.iterdir())

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, i):
        return np.load(self.file_paths[i])["arr_0"]


class BatchedRatingsIterator:
    def __init__(self, path, batch_size, total):
        self.ratings_iterable = RatingsIterable(path)
        self.batch_size = batch_size
        self.total = total

    def __len__(self):
        quotient, remainder = divmod(self.total, self.batch_size)
        return quotient + int(remainder != 0)

    def __iter__(self):
        i = 0
        iterable = iter(self.ratings_iterable)
        ratings = next(iterable)
        residual = None

        while True:

            if i + self.batch_size < len(ratings):
                if residual is None:
                    yield ratings[i : i + self.batch_size]
                    i += self.batch_size
                else:
                    delta = self.batch_size - len(residual)
                    yield np.concatenate(
                        [residual, ratings[:delta]], axis=0,
                    )
                    i += delta
                    residual = None
            else:
                residual = ratings[i:]
                i = 0
                try:
                    ratings = next(iterable)
                except StopIteration:
                    yield residual
                    break

