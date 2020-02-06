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

        if not isinstance(path, Path):
            path = Path(path)

        if path:
            pass
        elif global_cache:
            path = Path("~").expanduser() / ".dataget" / self.name
        else:
            path = Path("data") / self.name

        self.path = path

    def get(self, clean: bool = False, **kwargs):

        if clean or not self.is_valid(**kwargs):
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

        return self.load(**kwargs)

    @abstractmethod
    def download(self, **kwargs):
        pass

    @abstractmethod
    def load(self, **kwargs):
        pass

    @abstractmethod
    def is_valid(self, **kwargs):
        pass


class DownloadError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

