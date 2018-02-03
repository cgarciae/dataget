#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of dataget.
# https://github.com/cgarciae/dataget

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, cgarciae <cgarcia.e88@gmail.com>
from __future__ import print_function, absolute_import, unicode_literals, division
from .version import __version__  # NOQA

from . import utils
from . import dataset
from .api import ls, data, get_path, DATASETS
from .dataset_loader import (
    load_custom_datasets, load_plugin_datasets, load_local_datasets)
from .functions import (
    load_images, split, batch_generator, epochs_batch_generator, 
    infinite_random_batch_generator )

load_custom_datasets(DATASETS)
load_plugin_datasets(DATASETS)
load_local_datasets(DATASETS)