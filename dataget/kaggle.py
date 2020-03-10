import subprocess
from pathlib import Path

import pandas as pd

from dataget import utils
from dataget.dataset import Dataset


class kaggle(Dataset):
    @property
    def name(self):
        name = self.kaggle_dataset if self.kaggle_dataset else self.kaggle_competition
        return f"kaggle_{name.replace('/', '_')}"

    def __init__(self, dataset: str = None, competition: str = None, **kwargs):
        """
        Create a Kaggle dataset. You have to specify either `dataset` or `competition`.

        Arguments:
            dataset: the id of the kaggle dataset in the format `username/dataset_name`.
            competition: the name of the kaggle competition.
            kwargs: common init kwargs.
        """
        assert (
            dataset is not None != competition is not None
        ), "Set either dataset or competition"

        self.kaggle_dataset = dataset
        self.kaggle_competition = competition

        super().__init__(**kwargs)

    def get(self, files: list, **kwargs):
        """
        Arguments:
            files: the list of files that will be loaded into memory
            kwargs: common arguments consumed by `download`
        """
        self.download(**kwargs)

        return self.load(files)

    def _download(self):

        if self.kaggle_dataset:
            cmd = (
                f"kaggle datasets download -p {self.path} --unzip {self.kaggle_dataset}"
            )
        else:
            cmd = f"kaggle competitions download -p {self.path} --unzip {self.kaggle_competition}"

        subprocess.check_call(cmd, shell=True)

        if self.kaggle_competition:
            zip_path = self.path / f"{self.kaggle_competition}.zip"

            utils.ungzip(zip_path, self.path)
            zip_path.unlink()

    def load(self, files: list):
        return [self._load_file(filename) for filename in files]

    def _load_file(self, filename):
        filepath = self.path / filename

        if filepath.suffix == ".csv":
            df = pd.read_csv(filepath)
        else:
            raise ValueError(f"Extension not supported for '{filename}'")

        return df
