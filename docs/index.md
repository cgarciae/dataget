# Dataget

Dataget is an easy to use, framework-agnostic, dataset library that gives you quick access to a collection of Machine Learning datasets through a simple API.

Main features:

* **Minimal**: Downloads entire datasets with just 1 line of code.
* **Compatible**: Loads data as `numpy` arrays or `pandas` dataframes which can be easily used with the majority of Machine Learning frameworks.
* **Transparent**: By default stores the data in your current project so you can easily inspect it.
* **Memory Efficient**: When a dataset doesn't fit in memory it will return metadata instead you can iteratively load it.
* **Integrates with Kaggle**: Supports loading datasets directly from Kaggle in a variety of formats.

Checkout our list of [avaiable datasets](https://cgarciae.github.io/dataget/datasets/overview/).

## Getting Started

In dataget you just have to do two things:

* Select a dataset from the `data` module.
* Use the `get` method to download the data to disk and load it into memory.

```python
import dataget as dg


X_train, y_train, X_test, y_test = dg.data.vision.mnist().get()
```

This examples downloads the [MNIST](http://yann.lecun.com/exdb/mnist/) dataset to `./data/vision_mnist` and loads it as `numpy` arrays.

### Kaggle Support

Kaggle [promotes](https://www.kaggle.com/docs/datasets#supported-file-types) the use of `csv` files and `dataget` loves it! With dataget you can quickly download any dataset from the platform and have immediate access to the data:

```python
import dataget as dg

df_train, df_test = dg.data.kaggle("cristiangarcia/pointcloudmnist2d").get(
    files=["train.csv", "test.csv"]
)
```
To start using Kaggle datasets just make sure you have properly installed and configured the [Kaggle API](https://github.com/Kaggle/kaggle-api). In the future we want to expand Kaggle support in the following ways:

* Be able to load any file that `numpy` or `pandas` can read.
* Have generic support for other types of datasets like images, audio, video, etc. 
    * e.g `dg.data.kaggle(..., type="vision").get(...)`


## Installation

`dataget` is avaiable at [pypi](https://pypi.org/) so you can use your favorite package manager install to it:

#### pip
```bash
pip install dataget
```

#### pipenv
```bash
pipenv install pytest
```
#### poetry
```bash
poetry add dataget
```

## License
MIT License