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
### mnist example
```bash
pip install $(dataget reqs mnist)
```

```bash
dataget get -c mnist dims=20x20 format=jpg
```
### commands
```bash
> dataget --help

Usage: dataget [OPTIONS] COMMAND [ARGS]...

Options:
  -p, --path TEXT
  -g, --global_
  --help           Show this message and exit.

Commands:
  rm
  download
  extract
  get
  ls
  process
  rm_compressed
  rm_raw
  reqs
```

### get

```
> dataget get --help

Usage: dataget get [OPTIONS] DATASET [KWARGS]...

  performs the operations download, extract, rm_compressed, processes
  and rm_raw, in sequence. KWARGS must be in the form: key=value, and
  are fowarded to all opeartions.

Options:
  -c, --rm        removes the dataset's folder (if it exists) before
                     downloading
  --keep-compressed  keeps the compressed files: skips rm_compressed
  --dont-process     skips process
  --keep-raw         keeps the raw/unprocessed files: skips rm_raw
  --help             Show this message and exit.
```
This is the primary command you will use, it will perform the common operations needed to get the data in a usable format. By default it will create a `.dataget` folder in the current directory unless specified by the `dataget -g` flag. The data will live in `.dataget/data/{dataset}`. The following example
```bash
dataget get -c mnist dims=20x20 format=png
```
is *roughly* equivalent to
```bash
dataget download -c mnist
dataget extract mnist
dataget rm_compressed mnist
dataget process mnist dims=20x20 format=png
dataget rm_raw mnist
```

### ls
List all installed datasets
```bash
dataget ls
```
List all `dataget` datasets available for download
```bash
dataget ls -a
```
### -g
Use `dataget -g` to perform operations on the global 
```bash
dataget -g get mnist
```
```bash
dataget -g ls
```
## Python

## Contributing

### Template
```python
from dataget.core import DataSet, SubSet
from dataget.utils import get_file
import os, urllib, zipfile, sys, gzip

class MyDataSet(DataSet):

    def __init__(self, *args, **kwargs):
        super(MyDataSet, self).__init__(*args, **kwargs)

        # self.path
        # self.training_set
        # self.training_set.path
        # self.training_set.make_dirs()
        # self.test_set
        # self.test_set.path
        # self.test_set.make_dirs()


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
        self.training_set.make_dirs()
        self.test_set.make_dirs()

    def _extract(self, **kwargs):
        # extract the data
        pass

    def _rm_compressed(self, **kwargs):
        # remove the compressed files
        pass

    def _process(self, **kwargs):
        # process the data if needed
        pass

    def _rm_raw(self, **kwargs):
        # remove the raw data if needed
        pass


class MySetBase(SubSet):

    #self.path
    #self.make_dirs()

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
           #self.make_dirs()


class TestSetMyDataSet(MySetBase):

      def __init__(self, dataset, **kwargs):
          super(TestSetMyDataSet, self).__init__(dataset, "test-set", **kwargs)
          #self.path
          #self.make_dirs()

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
