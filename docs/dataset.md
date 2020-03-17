
# Creating a Dataset

The `Dataset` class defined these 3 abstract methods which you must implement:

* `name`: a property that returns the folder name of the dataset e.g. `image_mnist`.
* `download`: a method that downloads the data to disk and possibly perform other tasks such as file extraction, organization, and cleanup.
* `load`: the method that loads the data into memory and structures it in the most convenient format for the user.


!!! path
    The `self.path` field is a `pathlib.Path` that tells the dataset where the data should be stored. The `get` method ensures this path exists before calling `download` or `load`; use this field when implementing these methods.

### get kwargs
The `get` method will accept `**kwargs` which it will forward to `load`. For example:

```python
def load(self, dtype=np.float32):
    # code
```

With this implementation the `get` method can be called like this:

```python
.get(dtype=np.uint8)
```

### Template

You can use this template to get started. 

```python
from dataget.dataset import Dataset

class some_dataset(Dataset):

    # OPTIONAL
    def __init__(self, init_arg, **kwargs):
        # code
        super().__init__(**kwargs) # !!IMPORTANT
    
    @property
    def name(self):
        return "{dataset_type}_{dataset_name}"

    def download(self):
        # code 

    def load(self, some_arg):
        # code
        return a, b, c, ...
```

!!! warning
    If you are defining your own `__init__` remenber to always forward `**kwargs` to `super().__init__` since its very important that all datasets support the `path` and `global_cache` keyword arguments defined in the `Dataset` class. If `super().__init__` is not called at all the `path` field will not be instantiated and errors will occure.
