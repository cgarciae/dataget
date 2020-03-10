import asyncio
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from dataget import utils


class Dataset(ABC):
    """
    DATASETTTT
    """

    @property
    @abstractmethod
    def name(self):
        pass

    def __init__(self, path: Path = None, global_cache: bool = False):

        if path and not isinstance(path, Path):
            path = Path(path)

        if path:
            pass
        elif global_cache:
            path = Path("~").expanduser() / ".dataget" / self.name
        else:
            path = Path("data") / self.name

        self.path = path

    def get(self, clean: bool = False, debug: bool = False, **kwargs):
        if clean or not self.is_valid():

            if not debug:
                shutil.rmtree(self.path, ignore_errors=True)
                self.path.mkdir(parents=True)

            # get data
            coro = self.download()

            if coro is not None:
                asyncio.run(coro)

            # mark as valid
            (self.path / ".valid").touch()

        return self.load(**kwargs)

    def is_valid(self):
        return (self.path / ".valid").exists()

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def load(self):
        pass


class DownloadError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
