import asyncio
import gzip
import os
import re
from functools import partial, wraps
from pathlib import Path
from zipfile import ZipFile
import tarfile

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


def unzip(src_path, dst_path):

    with ZipFile(src_path, "r") as f:
        # Extract all the contents of zip file in current directory
        f.extractall(path=dst_path)


def untar(src_path, dst_path, fast=False, show_progress: bool = True):

    with tarfile.open(src_path, "r:gz") as f:

        if fast:
            f.extractall(path=dst_path)
        else:
            if show_progress:
                bar = tqdm(desc=f"Extracting {src_path.name}")

            member = True

            while member:
                member = f.next()
                f.extract(member, path=dst_path / member.name)

                if show_progress:
                    bar.update()


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

        total = show_progress and response.headers.get("Content-Length", None)

        if total:
            desc = path.name
            progress = tqdm(
                total=int(total),
                desc=f"Downloading {desc}",
                bar_format="{desc}:{percentage:3.0f}%|{bar}|{n:.2f}MB/{total:.2f}MB [{elapsed}<{remaining},{rate_noinv_fmt}]",
                unit_scale=1 / (1024 ** 2),
                unit="MB",
                smoothing=0.05,
            )

        async with aiofiles.open(path, "ab") as f:
            async for chunk in response.aiter_bytes():
                if total:
                    progress.update(n=len(chunk))

                await f.write(chunk)
