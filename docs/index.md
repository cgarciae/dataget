# Dataget

Dataget is an easy to use, framework agnostic dataset library that gives you quick access to a collection of Machine Learning datasets through a simple API.

* **Minimal**: Downloads entire datasets with just 1 line of code.
* **Compatible**: Loads data as `numpy` arrays or `pandas` dataframes which can be easily used with the majority of Machine Learning frameworks.
* **Transparent**: By default stores the data in your current project so you can easily inspect it.
* **Memory Efficient**: When a dataset doesn't fit in memory it will return the metadata needed so it can be loaded iteratively.
* **Integrates with Kaggle**: Supports loading Datasets directly from Kaggle in a variety of formats.

## Getting Started

In dataget you just have to use two functions:

* `data` to specify source of the data.
* `get` to download the dataset to disk and load it into memory.

```python
import dataget as dg


df_train, df_test = dg.data("mnist").get()
```

This examples downloads the [MNIST](http://yann.lecun.com/exdb/mnist/) to `./data/mnist` and loads it as `pandas` dataframes.

## Installation

```bash
pip install dataget
```