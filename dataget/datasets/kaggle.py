import subprocess
from pathlib import Path

import pandas as pd

from dataget import utils
from dataget.api import register_dataset
from dataget.datasets.dataset import Dataset


@register_dataset("kaggle")
class Kaggle(Dataset):
    def __init__(self, root: Path, dataset: str):
        if not isinstance(root, Path):
            root = Path(root)

        self.path = root / (
            self.name.replace("/", "_") + "_" + dataset.replace("/", "_")
        )
        self.kaggle_dataset = dataset

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

