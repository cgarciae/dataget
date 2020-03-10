# Dataget

Dataget is an easy to use, framework-agnostic, dataset library that gives you quick access to a collection of Machine Learning datasets through a simple API.

Main features:

* **Minimal**: Downloads entire datasets with just 1 line of code.
* **Compatible**: Loads data as `numpy` arrays or `pandas` dataframes which can be easily used with the majority of Machine Learning frameworks.
* **Transparent**: By default stores the data in your current project so you can easily inspect it.
* **Memory Efficient**: When a dataset doesn't fit in memory it will return metadata instead so you can iteratively load it.
* **Integrates with Kaggle**: Supports loading datasets directly from Kaggle in a variety of formats.

Checkout the [documentation](https://cgarciae.github.io/dataget/) for the list of available datasets.

## Getting Started

In dataget you just have to do two things:

* Instantiate a `Dataset` from our collection.
* Call the `get` method to download the data to disk and load it into memory.

Both are usually done in one line:

```python
import dataget


X_train, y_train, X_test, y_test = dataget.image.mnist().get()
```

This example downloads the [MNIST](http://yann.lecun.com/exdb/mnist/) dataset to `./data/image_mnist` and loads it as `numpy` arrays.

### Kaggle Support

Kaggle [promotes](https://www.kaggle.com/docs/datasets#supported-file-types) the use of `csv` files and `dataget` loves it! With dataget you can quickly download any dataset from the platform and have immediate access to the data:

```python
import dataget

df_train, df_test = dataget.kaggle("cristiangarcia/pointcloudmnist2d").get(
    files=["train.csv", "test.csv"]
)
```
To start using Kaggle datasets just make sure you have properly installed and configured the [Kaggle API](https://github.com/Kaggle/kaggle-api). In the future we want to expand Kaggle support in the following ways:

* Be able to load any file that `numpy` or `pandas` can read.
* Have generic support for other types of datasets like images, audio, video, etc. 
    * e.g `dataget.data.kaggle(..., type="image").get(...)`


## Installation

`dataget` is available at [pypi](https://pypi.org/) so you can use your favorite package manager.

##### pip
```bash
pip install dataget
```

##### pipenv
```bash
pipenv install pytest
```
##### poetry
```bash
poetry add dataget
```

## Contributing

Read our guide on [Creating a Dataset](https://cgarciae.github.io/dataget/dataset/) if you are interested in adding a dataset to dataget.

## License
MIT License
