import subprocess
from pathlib import Path

import pandas as pd

from dataget import utils
from dataget.dataset import Dataset


class kaggle(Dataset):
    @property
    def name(self):
        return f"kaggle_{self.kaggle_dataset.replace('/', '_')}"

    def __init__(self, dataset: str, **kwargs):
        self.kaggle_dataset = dataset

        super().__init__(**kwargs)

    def download(self, **kwargs):
        subprocess.check_call(
            f"kaggle datasets download -p {self.path} --unzip {self.kaggle_dataset}",
            shell=True,
        )

    def load_data(self, files, **kwargs):
        return [self._load_file(filename) for filename in files]

    def _load_file(self, filename):
        filepath = self.path / filename

        if filepath.suffix == ".csv":
            df = pd.read_csv(filepath)
        else:
            raise ValueError(f"Extension not supported for '{filename}'")

        return df

    def is_valid(self, files, **kwargs):
        return all((self.path / filename).exists() for filename in files)

