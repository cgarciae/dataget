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

    async def download(self):
        async with httpx.AsyncClient() as client:
            await asyncio.gather(
                utils.download_file(client, TRAIN_URL, self.path / "train.csv"),
                utils.download_file(client, TEST_URL, self.path / "test.csv"),
            )

    def load(self):
        return (
            pd.read_csv(self.path / "train.csv"),
            pd.read_csv(self.path / "test.csv"),
        )


if __name__ == "__main__":
    spirals().get()
