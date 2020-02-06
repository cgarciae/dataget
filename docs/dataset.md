
# Creating a Dataset

The `Dataset` class defined these 4 abstract methods which you must implement:

* `name`: a property that should return the name of the dataset e.g. `vision_mnist`.
* `download`: the method that should download the dataset to disk and possibly perform other tasks such as file extraction, organization, and cleanup.
* `load`: the method that loads the data into memory and possibly structures it in the most convenient format for the user.
* `is_valid`: a method which validates that the data on disk is valid to guarantee that the download process succeded.


!!! path
    The `self.path` field is a `pathlib.Path` that tells the dataset where the data should be stored. The `get` method ensures this path exists before calling `is_valid`, `download`, or `load`; use this field when implementing these methods.

### get kwargs
The `get` method will accept `**kwargs` which it will forward to `download`, `load`, and `is_valid` so all these methods have to accept the same arguments. An alternatively strategy is have each accept its desired required or optional arguments and accept `**kwargs` to accumulate the additional it doesn't need. For example:

```python
def download(self, version, limit=None, **kwargs):
    # code

def load(self, dtype=np.float32, **kwargs):
    # code
```

With this implementation you the `get` method could be called like this:

```python
.get(version="0.0.2", dtype=np.uint8)
```

!!! note
    In the previous example the `version` argument is required because `download` uses it as a positional argument although for `get` its just a keyword argument, if it were not passed a `TypeError` would've been raised.

### Template

You can use this template to get started. 

```python
from dataget.dataset import Dataset

class SomeDataset(Dataset):

    # OPTIONAL
    def __init__(self, init_arg, **kwargs):
        # code
        super().__init__(**kwargs) # !!IMPORTANT
    
    @property
    def name(self):
        return "some_dataset_name"

    def download(self, some_arg, **kwargs):
        # code 

    def load(self, other_arg, **kwargs):
        # code
        return data1, data2, data3, ...

    def is_valid(self, another_arg, **kwargs):
        # code
        return True | False
```

!!! warning
    If you are definint you own `__init__` remenber to always forward `**kwargs` to `super().__init__` since its important that all datasets support the `root` and `use_global` keyword arguments defined in the `Dataset` class. If `super().__init__` is not called at all the `path` field will not be instantiated and errors will occure.