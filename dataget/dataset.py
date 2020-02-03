import asyncio
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from dataget import utils


class Dataset(ABC):
    def __init__(self, root: Path):
        if not isinstance(root, Path):
            root = Path(root)

        self.path = root / self.name

    def get(self, use_cache=True, extras=None, **kwargs):

        # rm
        if not self.is_valid(**kwargs) or not use_cache:
            shutil.rmtree(self.path, ignore_errors=True)
            self.path.mkdir(parents=True)

            # get data
            coro = self.download(**kwargs)

            if coro is not None:
                asyncio.get_event_loop().run_until_complete(coro)

        outputs = self.load_data(extras, **kwargs)

        if extras and len(outputs) == 2:
            return outputs + (None,)
        else:
            return outputs

    @property
    def name(self):
        return utils.upper_to_dashed(self.__class__.__name__)

    @abstractmethod
    def download(self, **kwargs):
        pass

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def is_valid(self):
        pass
