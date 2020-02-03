import subprocess
from pathlib import Path

import pandas as pd

from dataget import utils
from dataget.api import register_dataset
from dataget.dataset import Dataset


class Kaggle(Dataset):
    def __init__(self, root: Path, dataset: str):
        if not isinstance(root, Path):
            root = Path(root)

        self.path = root / self.name / dataset
        self.kaggle_dataset = dataset

    def download(self, **kwargs):
        subprocess.check_call(
            f"kaggle datasets download -p {self.path} --unzip {self.kaggle_dataset}",
            shell=True,
        )

    def load_data(self, extras, train_file, test_file=None, **kwargs):

        df_train = self._load_file(train_file)

        if test_file is None:
            df_test = None
        else:
            df_test = self._load_file(test_file)

        outputs = (df_train, df_test)

        if extras:
            extras = {filename: self._load_file(filename) for filename in extras}
            outputs += (extras,)

        return outputs

    def _load_file(self, filename):
        filepath = self.path / filename

        if filepath.suffix == ".csv":
            df = pd.read_csv(filepath)
        else:
            raise ValueError(f"Extension not supported for '{filename}'")

        return df

    def is_valid(self, train_file, test_file=None, **kwargs):

        validity = (self.path / train_file).exists()

        if test_file:
            validity = validity and (self.path / test_file).exists()

        return validity


if __name__ == "__main__":

    df_train, df_test = Kaggle("data", dataset="cristiangarcia/pointcloudmnist2d").get(
        train_file="train.csv", test_file="test.csv"
    )

    print(df_train.shape)
    print(df_test.shape)

