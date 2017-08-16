#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xad823ee2

# Compiled with Coconut version 1.2.3-post_dev5 [Colonel]

# Coconut Header: --------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------------

import os
import re
import platform
from six.moves import urllib



OS_SPLITTER = "/" if not platform.system() == "Windows" else "\\"

def get_progress(filename):
    def progress(count, blockSize, totalSize):

        new = int(count * blockSize * 100 / totalSize)

        if new % 5 == 0 and new != progress.last:
            print("{} {}%".format(filename, new))
            progress.last = new

    progress.last = -1

    return progress

def get_file(file_url, path, filename=None, print_info=True):
    if filename is None:
        filename = file_url.split("/")[-1]

    file_path = os.path.join(path, filename)

    if print_info:
        print("downloading {}".format(filename))

    urllib.request.urlretrieve(file_url, file_path, get_progress(filename))


def maybe_mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return path

def split_upper(txt):
    return [a for a in re.split(r'([A-Z][a-z]*\d*)', txt) if a]

def upper_to_dashed(txt):
    return ("-".join)((_coconut.functools.partial(map, _coconut.operator.methodcaller("lower")))((split_upper)(txt)))


def read_pillow_image(Image, np):
    def _read_pillow_image(filename):
        with Image.open(filename) as im:
            return np.asarray(im, dtype=np.uint8)

    return _read_pillow_image


def move_files(files, folder_orig, folder_dst):
    for file in files:
        os.rename(os.path.join(folder_orig, file), os.path.join(folder_dst, file))
