import asyncio

import httpx
import pandas as pd

from dataget import utils
from dataget.dataset import Dataset

TRAIN_URL = "https://raw.githubusercontent.com/colomb-ia/supervised-basico-spirals/master/training-set.csv"
TEST_URL = "https://raw.githubusercontent.com/colomb-ia/supervised-basico-spirals/master/test-set.csv"


class spirals(Dataset):
    @property
    def name(self):
        return "toy_spirals"

    async def download(self, **kwargs):
        async with httpx.AsyncClient() as client:
            await asyncio.gather(
                asyncio.create_task(
                    utils.download_file(client, TRAIN_URL, self.path / "train.csv"),
                ),
                asyncio.create_task(
                    utils.download_file(client, TEST_URL, self.path / "test.csv"),
                ),
            )

    def load(self, **kwargs):
        return (
            pd.read_csv(self.path / "train.csv"),
            pd.read_csv(self.path / "test.csv"),
        )

    def is_valid(self, **kwargs):
        return all(
            [(self.path / "train.csv").exists(), (self.path / "test.csv").exists(),]
        )


if __name__ == "__main__":
    spirals().get()
