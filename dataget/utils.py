import asyncio
import gzip
import re
from pathlib import Path

import aiofiles
import httpx
from tqdm import tqdm
import asyncio
from functools import partial, wraps
import os

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


def ungzip(src_name, dest_name):

    with gzip.open(src_name, "rb") as infile:
        with open(dest_name, "wb") as outfile:
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
            progress = tqdm(
                total=int(total),
                desc=f"Downloading {url}",
                bar_format="{desc}:{percentage:3.0f}%|{bar}|{n:.2f}MB/{total:.2f}MB [{elapsed}<{remaining},{rate_noinv_fmt}]",
                unit_scale=1 / (1024 ** 2),
                unit="MB",
            )

        async with aiofiles.open(path, "ab") as f:
            async for chunk in response.aiter_bytes():
                if total:
                    progress.update(n=len(chunk))

                await f.write(chunk)
