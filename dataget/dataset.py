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

    def get(self, clean: bool = False, debug: bool = False):
        self.download(clean=clean, debug=clean)

        return self.load()

    def download(self, clean: bool = False, debug: bool = False, **kwargs):

        if clean or not self.is_valid():

            if not debug:
                shutil.rmtree(self.path, ignore_errors=True)
                self.path.mkdir(parents=True)

            # get data
            coro = self._download(**kwargs)

            if coro is not None:
                asyncio.run(coro)

            # mark as valid
            (self.path / ".valid").touch()

    def is_valid(self):
        return (self.path / ".valid").exists()

    @abstractmethod
    def _download(self, **kwargs):
        pass

    @abstractmethod
    def load(self, **kwargs):
        pass


class DownloadError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
