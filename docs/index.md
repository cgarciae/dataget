# Dataget

Dataget is an easy to use, framework-agnostic, dataset library that gives you quick access to a collection of Machine Learning datasets through a simple API.

Main features:

* **Minimal**: Downloads entire datasets with just 1 line of code.
* **Compatible**: Loads data as `numpy` arrays or `pandas` dataframes which can be easily used with the majority of Machine Learning frameworks.
* **Transparent**: By default stores the data in your current project so you can easily inspect it.
* **Memory Efficient**: When a dataset doesn't fit in memory it will instead return the metadata needed so it can be iteratively loaded.
* **Integrates with Kaggle**: Supports loading Datasets directly from Kaggle in a variety of formats.

## Getting Started

In dataget you just have to use two functions:

* `data` to specify source of the data.
* `get` to download the dataset to disk and load it into memory.

```python
import dataget as dg


X_train, y_train, X_test, y_test = dg.data("vision/mnist").get()
```

This examples downloads the [MNIST](http://yann.lecun.com/exdb/mnist/) to `./data/vision_mnist` and loads it as `numpy` arrays.

### Kaggle

Kaggle promotes the use of `csv` files and `dataget` loves it! 

```python
import dataget as dg

df_train, df_test = dg.data(
    "kaggle", dataset="cristiangarcia/pointcloudmnist2d"
).get(files=["train.csv", "test.csv"])
```

In the future we want to expand Kaggle support in the following ways:

* Be able to load any file that `numpy` or `pandas` can read.
* Have generic support for other types of datasets like images, audio, or video. E.g. `dg.get("kaggle/vision", ...).get(...)`

## Installation

Avaiable at `pypi` as `dataget`, you can install it with your favorite python package manager:

```bash
# pip
pip install dataget

# pipenv
pipenv install pytest

# poetry
poetry add dataget
```