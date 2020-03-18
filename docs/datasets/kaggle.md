
# dataget.kaggle

Download any dataset from the Kaggle platform and immediately loads it into memory:

```python
import dataget

df_train, df_test = dataget.kaggle(dataset="cristiangarcia/pointcloudmnist2d").get(
    files=["train.csv", "test.csv"]
)
```

In this example we downloaded the [Point Cloud Mnist 2D](https://www.kaggle.com/cristiangarcia/pointcloudmnist2d) dataset from Kaggle and load the `train.csv` and `test.csv` files as `pandas` dataframes.

!!! info "Config"
    To start using this `Dataset` make sure you have properly installed and configured the [Kaggle API](https://github.com/Kaggle/kaggle-api).


## Supported Formats

Right now we only support the `csv` format. In the future we want to be able to load any file that `numpy` or `pandas` can read.

## API Reference
::: dataget.kaggle