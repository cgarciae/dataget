from __future__ import absolute_import, unicode_literals, division
import pandas as pd
from PIL import Image


def load_image(filename):
    try:
        with Image.open(filename) as img:
            return np.asarray(img)
    except IOError:
        return None

def load_images(df, path_key = "filename", image_key = "image"):
    df[image_key]


