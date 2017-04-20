#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xe9d9f6c8

# Compiled with Coconut version 1.2.2-post_dev12 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------

import urllib
import os

def get_progress():
    def progress(count, blockSize, totalSize):

        new = int(count * blockSize * 100 / totalSize)

        if new % 5 == 0 and new != progress.last:
            print("{}%".format(new))
            progress.last = new

    progress.last = -1

    return progress

def get_file(file_url, path, filename=None, print_info=True):
    if filename is None:
        filename = file_url.split("/")[-1]

    file_path = os.path.join(path, filename)

    if print_info:
        print("downloading {}".format(filename))

    url_opener = urllib.URLopener()
    url_opener.retrieve(file_url, file_path, get_progress())
    url_opener.close()


def maybe_mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return path
