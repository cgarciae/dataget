import asyncio
import copy
import gzip
import os
import re
import tarfile
from functools import partial, wraps
from pathlib import Path
from zipfile import ZipFile

import aiofiles
import httpx
from tqdm import tqdm

########################################################################
# aiofiles.os
########################################################################


def wrap(func):
    @asyncio.coroutine
    @wraps(func)
    def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return loop.run_in_executor(executor, pfunc)

    return run


stat = wrap(os.stat)
rename = wrap(os.rename)
remove = wrap(os.remove)
mkdir = wrap(os.mkdir)
rmdir = wrap(os.rmdir)

if hasattr(os, "sendfile"):
    sendfile = wrap(os.sendfile)

########################################################################


def unzip(src_path, dst_path, show_progress: bool = True):

    with ZipFile(src_path, "r") as f:
        if show_progress:
            # Loop over each file
            for file in tqdm(
                iterable=f.namelist(),
                total=len(f.namelist()),
                desc=f"Extracting {src_path.name}",
            ):

                # Extract each file to another directory
                # If you want to extract to current working directory, don't specify path
                f.extract(member=file, path=dst_path)
        else:
            # Extract all the contents of zip file in current directory
            f.extractall(path=dst_path)


def untar(src_path, dst_path, show_progress: bool = True):

    mode = "r:gz" if str(src_path).endswith("gz") else "r"

    with tarfile.open(src_path, mode) as f:

        if show_progress:

            directories = []

            for tarinfo in tqdm(f.getmembers(), desc=f"Extracting {src_path.name}"):
                if tarinfo.isdir():
                    # Extract directories with a safe mode.
                    directories.append(tarinfo)
                    tarinfo = copy.copy(tarinfo)
                    tarinfo.mode = 0o700
                # Do not set_attrs directories, as we will do that further down
                f.extract(
                    tarinfo, dst_path, set_attrs=not tarinfo.isdir(),
                )

            # Reverse sort directories.
            directories.sort(key=lambda a: a.name)
            directories.reverse()

            # Set correct owner, mtime and filemode on directories.
            for tarinfo in directories:
                dirpath = os.path.join(str(dst_path), tarinfo.name)
                try:
                    f.chown(tarinfo, dirpath, numeric_owner=False)
                    f.utime(tarinfo, dirpath)
                    f.chmod(tarinfo, dirpath)
                except tarfile.ExtractError as e:
                    if f.errorlevel > 1:
                        raise
                    else:
                        f._dbg(1, "tarfile: %s" % e)

        else:
            f.extractall(path=dst_path)


def ungzip(src_path, dst_path, show_progress: bool = True):

    with gzip.open(src_path, "rb") as infile:
        with open(dst_path, "wb") as outfile:
            for line in infile:
                outfile.write(line)


def split_upper(txt: str):
    return [a for a in re.split(r"([A-Z][a-z]*\d*)", txt) if a]


def upper_to_dashed(txt: str):

    txt = split_upper(txt)
    txt = map(lambda s: s.lower(), txt)

    return "-".join(txt)


async def run_in_executor(f):
    await asyncio.get_event_loop().run_in_executor(None, f)


async def download_file(
    client: httpx.AsyncClient, url: str, path: Path, show_progress: bool = True
):
    if path.exists():
        await remove(path)

    async with client.stream("GET", url) as response:

        content_length = response.headers.get("Content-Length", None)
        desc = path.name

        if show_progress and content_length:

            progress = tqdm(
                total=int(content_length),
                desc=f"Downloading {desc}",
                bar_format="{desc}:{percentage:3.0f}%|{bar}|{n:.2f}MB/{total:.2f}MB [{elapsed}<{remaining},{rate_noinv_fmt}]",
                unit_scale=1 / (1024 ** 2),
                unit="MB",
                smoothing=0.05,
            )
        else:
            print(f"Downloading {desc}...")

        async with aiofiles.open(path, "ab") as f:
            async for chunk in response.aiter_bytes():
                if show_progress and content_length:
                    progress.update(n=len(chunk))

                await f.write(chunk)
