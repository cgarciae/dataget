import gzip
import re
from pathlib import Path

import aiofiles
import httpx
from tqdm import tqdm


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


async def download_file(
    client: httpx.AsyncClient, url: str, path: Path, show_progress: bool = True
):
    if path.exists():
        await aiofiles.os.remove(path)

    async with client.stream("GET", url) as response:

        total = show_progress and response.headers.get("Content-Length", None)

        if total:
            progress = tqdm(total=int(total), desc=f"Downloading {url}")

        async with aiofiles.open(path, "ab") as f:
            async for chunk in response.aiter_bytes():
                if total:
                    progress.update(n=len(chunk))

                await f.write(chunk)
