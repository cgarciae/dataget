#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x251674eb

# Compiled with Coconut version 1.2.3-post_dev1 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of dataget.
# https://github.com/cgarciae/dataget

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, cgarciae <cgarcia.e88@gmail.com>

from .version import __version__  # NOQA

from . import utils
from . import dataset
from .api import ls
from .api import data
from .api import get_path
from .api import DATASETS
from .dataset_loader import load_custom_datasets
from .dataset_loader import load_plugin_datasets


def print_hello():
    import time
    time.sleep(1)
    print("HELLO WORLD")
    time.sleep(1)


load_custom_datasets(DATASETS)
load_plugin_datasets(DATASETS)
