# dataget

`dataget` is a Bash and Python library that helps you download popular, organize and process popular machine learning datasets. Its goal is to make readily available as many ML datasets as posible to users of any language. For Python users it also had the added benefits of exposing an interface to access the `training-set` and `test-set` as `pandas` dataframes or `numpy` arrays, and also random batch generators of the previous for large datasets. See

* [Bash Client](#bash)
* [Python Library](#python)

## Getting Started
While `dataget` is intended for users of any language you need `python` and `pip` to install `dataget` itself and some dependencies required by each dataset.

### Instalation
```bash
pip install dataget
```

## Bash


### Hello World

## Python

## Contributing

### Template
```python
from dataget.dataset import DataSet, SubSet


class GermanTrafficSignsDataset(DataSet):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        # self.path
        # self.training_set
        # self.training_set.path
        # self.test_set
        # self.test_set.path


    @property
    def training_set_class(self):
        return TrainingSetMyDataSet

    @property
    def test_set_class(self):
        return TestSetMyDataSet

    @property
    def help(self):
        return "" # information for the help command

    def reqs(self, **kwargs):
        return "" # e.g. "numpy pandas pillow"


    def _download(self, **kwargs):
        # download the data, propably a compressed format

    def _extract(self, **kwargs):
        # extract the data

    def _remove_compressed(self, **kwargs):
        # remove the compressed files

    def _process(self, **kwargs):
        # process the data if needed

    def _remove_raw(self, **kwargs):
        # remove the raw data if needed


class MySetBase(SubSet):

    #self.path

    def dataframe(self):
        # code
        return df


    def arrays(self):
        # code
        return features, labels


    def random_batch_dataframe_generator(self, batch_size):
        # code
        yield df


    def random_batch_arrays_generator(self, batch_size):
        # code
        yield features, labels


class TrainingSetMyDataSet(MySetBase):


       def __init__(self, dataset, **kwargs):
           super(TrainingSetMyDataSet, self).__init__(dataset, "training-set", **kwargs)
           #self.path


class TestSetMyDataSet(TestSet):

      def __init__(self, dataset, **kwargs):
          super(TestSetMyDataSet, self).__init__(dataset, "test-set", **kwargs)
          #self.path

```

## Example
### Simple
Using bash
```bash
dataget load german-traffic-signs #download, extract and cleanup folder
dataget process german-traffic-signs #process (convert to 32x32 jpg)
```
Using python
```python
from dataget import data
signs = data("german-traffic-signs") #download, extract and cleanup folder
signs.load().process() #process (convert to 32x32 jpg)
```

### More control
Using bash
```bash
dataget download german-traffic-signs #download
dataget extract german-traffic-signs #extract
dataget remove-sources german-traffic-signs #cleanup folder
dataget process german-traffic-signs #process (convert to 32x32 jpg)
```

Using python
```python
from dataget import data
signs = data("german-traffic-signs")
signs.download() #download
signs.extract() #extract
signs.remove_sources() #cleanup folder
signs.process() #process (convert to 32x32 jpg)
```

### Params
Using bash
```bash
dataget process german-traffic-signs -p dims:40x40 #process (convert to 40x40 jpg)
```
Using python
```python
from dataget import data
signs = data("german-traffic-signs") #download, extract and cleanup folder
signs.process(dims="40x40") #process (convert to 32x32 jpg)
```

### Numpy and Pandas
Assuming you already downloaded the data, you can
```python
from dataget import data
signs = data("german-traffic-signs") #download, extract and cleanup folder

df = signs.training_set.datafame()
```
