#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x976095a

# Compiled with Coconut version 1.2.3 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division


# Compiled Coconut: ------------------------------------------------------

import click
click.disable_unicode_literals_warning = True

import os

from dataget.api import ls as _ls
from dataget.api import data
from dataget.api import get_path
from dataget import api

@click.group()
@click.option('--path', '-p', default=None)
@click.pass_context
def main(ctx, path):
    path = get_path(path=path)
    ctx.obj = dict(path=path)


@main.command()
@click.option('--installed', '-i', is_flag=True, help="List all available dataget datasets for download.")
@click.pass_context
def ls(ctx, installed):
    "List installed datasets on path"

    for dataset in api.ls(installed=installed):
        print(dataset)

@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def reqs(ctx, dataset, kwargs):
    "Get the dataset's pip requirements"

    kwargs = _parse_kwargs(kwargs)
    reqs = data(dataset, **ctx.obj).reqs(**kwargs)
    
    print(reqs)


@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def size(ctx, dataset, kwargs):
    "Show dataset size"

    kwargs = _parse_kwargs(kwargs)
    df = data(dataset, **ctx.obj).get(**kwargs).df

    print(len(df))


@main.command()
@click.argument('dataset')
@click.option('--rm', '-r', is_flag=True, help="removes the dataset's folder (if it exists) before downloading")
@click.option('--keep-compressed', is_flag=True, help="keeps the compressed files: skips rm_compressed")
@click.option('--dont-process', is_flag=True, help="skips process")
@click.option('--dont-download', is_flag=True, help="skips download")
@click.option('--keep-raw', is_flag=True, help="keeps the raw/unprocessed files: skips rm_raw")
@click.argument('kwargs', nargs=-1)
@click.pass_context
def get(ctx, dataset, rm, keep_compressed, dont_process, dont_download, keep_raw, kwargs):
    "performs the operations download, extract, rm_compressed, processes and rm_raw, in sequence. KWARGS must be in the form: key=value, and are fowarded to all opeartions."

    kwargs = _parse_kwargs(kwargs)

    process = not dont_process
    rm_raw = not keep_raw
    rm_compressed = not keep_compressed
    download = not dont_download

    data(dataset, **ctx.obj).get(download=download, rm=rm, rm_compressed=rm_compressed, process=process, rm_raw=rm_raw, **kwargs)


@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm(ctx, dataset, kwargs):
    "removes the dataset's folder if it exists"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).rm(**kwargs)

@main.command("rm-subsets")
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm_subsets(ctx, dataset, kwargs):
    "removes the dataset's training-set and test-set folders if they exists"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).rm_subsets(**kwargs)

@main.command()
@click.argument('dataset')
@click.option('--rm', '-r', is_flag=True, help="removes the dataset's folder if it exists before downloading")
@click.argument('kwargs', nargs=-1)
@click.pass_context
def download(ctx, dataset, rm, kwargs):
    "downloads the dataset's compressed files"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).download(rm=rm, **kwargs)

@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def extract(ctx, dataset, kwargs):
    "extracts the files from the compressed archives"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).extract(**kwargs)


@main.command("rm-compressed")
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm_compressed(ctx, dataset, kwargs):
    "removes the compressed files"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).rm_compressed(**kwargs)

@main.command()
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def process(ctx, dataset, kwargs):
    "processes the data to a friendly format"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).process(**kwargs)


@main.command("rm-raw")
@click.argument('dataset')
@click.argument('kwargs', nargs=-1)
@click.pass_context
def rm_raw(ctx, dataset, kwargs):
    "removes the raw unprocessed data"

    kwargs = _parse_kwargs(kwargs)
    data(dataset, **ctx.obj).rm_raw(**kwargs)



def _parse_kwargs(kwargs):

    kwargs = map(lambda arg: arg.split("="), kwargs)
    kwargs = map(tuple, kwargs)

    return dict(kwargs)