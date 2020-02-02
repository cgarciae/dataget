#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa5321268

# Compiled with Coconut version 1.2.3 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division



# Compiled Coconut: ------------------------------------------------------

import os
import re
import platform
from six.moves import urllib

from tqdm import tqdm
import requests
import math






OS_SPLITTER = os.sep

def get_progress(filename):
    def progress(count, blockSize, totalSize):

        new = int(count * blockSize * 100 / totalSize)

        if new % 5 == 0 and new != progress.last:
            print("{} {}%".format(filename, new))
            progress.last = new

    progress.last = -1

    return progress

def get_file(url, path, filename=None, print_info=True):

    if filename is None:
        filename = os.path.basename(url)

    file_path = os.path.join(path, filename)
    
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024

    wrote = 0
    with open(file_path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")  


def get_path(name=None, path=None):

    if path:
        return os.path.realpath(path)

    path = os.environ.get(
        "DATAGET_HOME", 
        os.path.expanduser(os.path.join("~", ".dataget")),
    )

    path = os.path.join(path, "data")
    path = os.path.realpath(path)

    if name:
        path = os.path.join(path, name)

    return path


def maybe_mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return path

def split_upper(txt):
    return [a for a in re.split(r'([A-Z][a-z]*\d*)', txt) if a]

def upper_to_dashed(txt):
    
    txt = split_upper(txt)
    txt = map(lambda s: s.lower(), txt)

    return "-".join(txt)


def read_pillow_image(Image, np):
    def _read_pillow_image(filename):
        with Image.open(filename) as im:
            return np.asarray(im, dtype=np.uint8)

    return _read_pillow_image


def move_files(files, folder_orig, folder_dst):
    for file in files:
        move_file(file, folder_orig, folder_dst)

def move_file(filename, folder_orig, folder_dst):
    os.rename(os.path.join(folder_orig, filename), os.path.join(folder_dst, filename))
