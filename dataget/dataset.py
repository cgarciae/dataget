import asyncio
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
import typing as tp

from dataget import utils


class Dataset(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    def __init__(self, path: Path = None, global_cache: bool = False):
        """
        By default every dataset is downloaded inside `./data/{dataset_name}` in the current directory, however, you can use the the parameters from the base `dataget.Dataset` class constructor to constrol where the data is stored.

        Parameters:
            path: if set defines the exact location where the dataset will be stored. Takes precedence over `global_cache`.
            global_cache: if `True` the data is downloaded to `~/.dataget/{dataset_name}` instead. Use this to reuse datasets across projects.

        ### Examples

        Setting `global_cache=True` on any dataset constructor downloads the data to global folder:

        ```python
        dataget.image.mnist(global_cache=True).get()
        ```

        By setting the `path` argument you can specify the exact location for the dataset:

        ```python
        dataget.image.mnist(path="/my/dataset/path").get()
        ```
        """

        if path and not isinstance(path, Path):
            path = Path(path)

        if path:
            pass
        elif global_cache:
            path = Path("~").expanduser() / ".dataget" / self.name
        else:
            path = Path("data") / self.name

        self.path = path

    def get(self, clean: bool = False, _debug: bool = False, **kwargs):
        """
        Downloads and load the dataset into memory.

        Parameters:
            clean: deletes the dataset folder and forces a new download of the data.
            kwargs: all keyword arguments are forwarded to the `load` method. Consult the documentation on a specific dataset to see which options are available.

        """

        if clean or not self.is_valid():

            if not _debug:
                shutil.rmtree(self.path, ignore_errors=True)
                self.path.mkdir(parents=True)

            # get data
            coro = self.download()

            if isinstance(coro, tp.Awaitable):
                asyncio.new_event_loop().run_until_complete(coro)

            # mark as valid
            (self.path / ".valid").touch()

        return self.load(**kwargs)

    def is_valid(self):
        return (self.path / ".valid").exists()

    @abstractmethod
    def download(self) -> tp.Optional[tp.Awaitable]:
        pass

    @abstractmethod
    def load(self):
        pass


class DownloadError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
