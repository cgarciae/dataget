import os

import aiofiles
import httpx
import idx2numpy
import pandas as pd

from dataget import utils
from dataget.dataset import Dataset


class imdb_reviews(Dataset):
    @property
    def name(self):
        return "text_imdb_reviews"

    async def download(self):

        gz_path = self.path / "aclImdb_v1.tar.gz"

        async with httpx.AsyncClient() as client:

            await utils.download_file(
                client,
                "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz",
                gz_path,
            )

        utils.untar(gz_path, self.path)
        gz_path.unlink()

    def load(self, include_unlabeled=False):
        """
        Arguments:
            include_unlabeled: whether or not to include the unlabeled samples.
        """
        train_path = self.path / "aclImdb" / "train"
        test_path = self.path / "aclImdb" / "test"

        # train
        df_train = [
            self.load_df(train_path / "pos", label=1),
            self.load_df(train_path / "neg", label=0),
        ]

        if include_unlabeled:
            df_train.append(self.load_df(train_path / "unsup", label=-1))

        df_train = pd.concat(df_train, axis=0)

        # test
        df_test = pd.concat(
            [
                self.load_df(test_path / "pos", label=1),
                self.load_df(test_path / "neg", label=0),
            ],
            axis=0,
        )

        return df_train, df_test

    def load_df(self, path, label):
        file_paths = list(map(str, (path).iterdir()))
        df = pd.DataFrame(dict(text_path=file_paths))

        df["text"] = df["text_path"].map(lambda x: open(x).read())
        df["label"] = label

        return df
