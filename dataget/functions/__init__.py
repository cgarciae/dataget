from __future__ import absolute_import, unicode_literals, division

#%%
import pandas as pd
from PIL import Image
import numpy as np


def _load_image(filename):
    try:
        with Image.open(filename) as img:
            return np.asarray(img)
    except IOError:
        return None

def load_images(df, path_key = "filename", image_key = "image", inplace = False):
    """
    """
    
    if not inplace:
        df = df.copy()

    df[image_key] = df[path_key].apply(_load_image)

    return df

def shuffle(df, seed = None):
    """
    """

    if seed is not None:
        np.random.seed(seed = seed)

    return df.sample(frac = 1)

def split(df, *splits):
    """
    """


    splits = list(splits)

    if len(splits) == 0:
        raise Exception("Please insert at least one *splits paramter")
    elif len(splits) == 1:
        inverse = 1.0 - splits[0]
        splits.append(inverse)

    splits = [0.0] + list(splits)
    splits = np.asarray(splits)
    splits = np.cumsum(splits) / np.sum(splits)
    splits = len(df) * splits
    splits = np.round(splits).astype(np.int64)

    dfs = []

    for i in range(len(splits) - 1):
        a = splits[i]
        b = splits[i+1]

        split_df = df.iloc[a:b].copy()

        dfs.append(split_df)

    return dfs


def batch_generator(df, batch_size, shuffle = False):
    """
    """

    df = df.copy()

    if shuffle:
        df = df.sample(frac = 1.0)

    a = 0
    b = min(batch_size, len(df))

    while a < len(df):

        yield df.iloc[a:b].copy()

        a = b
        b = min(b + batch_size, len(df))

def epochs_batch_generator(df, batch_size, epochs, shuffle = False):
    """
    """

    for i in range(epochs):
        for batch in batch_generator(df, batch_size, shuffle = shuffle):
            yield batch

def infinite_random_batch_generator(df, batch_size):
    """
    """
    
    while True:
        yield df.sample(n = batch_size).copy()


