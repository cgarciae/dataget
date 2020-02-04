import asyncio
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from dataget import utils


class Dataset(ABC):

    name: str = None

    def __init__(self, root: Path):
        """
        ABC
        """
        assert self.name, f"Empty 'name' for class {self.__class__}"

        if not isinstance(root, Path):
            root = Path(root)

        self.path = root / self.name.replace("/", "_")

    def get(self, use_cache=True, **kwargs):
        """
        DFG
        """

        if not self.is_valid(**kwargs) or not use_cache:
            shutil.rmtree(self.path, ignore_errors=True)
            self.path.mkdir(parents=True)

            # get data
            coro = self.download(**kwargs)

            if coro is not None:
                asyncio.get_event_loop().run_until_complete(coro)

            if not self.is_valid(**kwargs):
                raise DownloadError(
                    f"Failed download for '{self.name}' at '{self.path}'"
                )

        return self.load_data(**kwargs)

    @abstractmethod
    def download(self, **kwargs):
        pass

    @abstractmethod
    def load_data(self, **kwargs):
        pass

    @abstractmethod
    def is_valid(self, **kwargs):
        pass


class DownloadError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

