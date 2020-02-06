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

    def __init__(self, root: Path = None, use_global: bool = False):

        if root:
            pass
        elif use_global:
            root = Path("~").expanduser() / ".dataget"
        else:
            root = Path("data")

        self.path = root / self.name

    def get(self, use_cache: bool = True, **kwargs):

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

