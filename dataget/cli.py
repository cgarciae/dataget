#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x388558a0

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

import click
click.disable_unicode_literals_warning = True

import os

from dataget.api import ls as _ls
from dataget.api import data
from dataget.api import get_path

@click.group()
@click.option('--path', '-p', default=None)
@click.option('-g', is_flag=True, help="Use global path: DATAGET_HOME env variable or ~/.dataget by default.")
@click.pass_context
def main(ctx, path, g):
    path = get_path(path=path, global_=g)
    ctx.obj = dict(path=path, global_=g)


@main.command()
@click.option('--available', '-a', is_flag=True, help="List all available dataget datasets for download.")
@click.pass_context
def ls(ctx, available):
    "List installed datasets on path"

    path = ctx.obj['path']
    global_ = ctx.obj['global_']

    _ls(available=available, path=path, global_=global_)

@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def reqs(ctx, dataset, kwargs):
    "Get the dataset's pip requirements"

    kwargs = parse_kwargs(kwargs)
    (print)(data(dataset, ctx.obj["path"]).reqs(**kwargs))


@main.command()
@click.argument('dataset')
@click.option('--rm', '-r', is_flag=True, help="removes the dataset's folder (if it exists) before downloading")
@click.option('--keep-compressed', is_flag=True, help="keeps the compressed files: skips rm_compressed")
@click.option('--dont-process', is_flag=True, help="skips process")
@click.option('--keep-raw', is_flag=True, help="keeps the raw/unprocessed files: skips rm_raw")
@click.argument('kwargs', nargs=-1)
@click.pass_context
def get(ctx, dataset, rm, keep_compressed, dont_process, keep_raw, kwargs):
    "performs the operations download, extract, rm_compressed, processes and rm_raw, in sequence. KWARGS must be in the form: key=value, and are fowarded to all opeartions."

    kwargs = parse_kwargs(kwargs)

    process = not dont_process
    rm_raw = not keep_raw
    rm_compressed = not keep_compressed

    data(dataset, ctx.obj["path"]).get(rm=rm, rm_compressed=rm_compressed, process=process, rm_raw=rm_raw, **kwargs)


@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm(ctx, dataset, kwargs):
    "removes the dataset's folder if it exists"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).rm(**kwargs)

@main.command("rm-subsets")
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm_subsets(ctx, dataset, kwargs):
    "removes the dataset's training-set and test-set folders if they exists"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).rm_subsets(**kwargs)

@main.command()
@click.argument('dataset')
@click.option('--rm', '-r', is_flag=True, help="removes the dataset's folder if it exists before downloading")
@click.argument('kwargs', nargs=-1)
@click.pass_context
def download(ctx, dataset, rm, kwargs):
    "downloads the dataset's compressed files"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).download(rm=rm, **kwargs)

@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def extract(ctx, dataset, kwargs):
    "extracts the files from the compressed archives"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).extract(**kwargs)


@main.command("rm-compressed")
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm_compressed(ctx, dataset, kwargs):
    "removes the compressed files"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).rm_compressed(**kwargs)

@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def process(ctx, dataset, kwargs):
    "processes the data to a friendly format"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).process(**kwargs)


@main.command("rm-raw")
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm_raw(ctx, dataset, kwargs):
    "removes the raw unprocessed data"

    kwargs = parse_kwargs(kwargs)
    data(dataset, ctx.obj["path"]).rm_raw(**kwargs)



def parse_kwargs(kwargs):
    return ((dict)((_coconut.functools.partial(map, tuple))((_coconut.functools.partial(map, _coconut.operator.methodcaller("split", "=")))(kwargs))))
