# Advanced Usage

## Specifying Download Directory

By default every dataset is downloaded inside a `./data/{dataset_name}` folder in the current directory. There are two ways you can control where the data is stored: the first one is use the `global_cache` keyword argument on the constructor of any `Dataset`

```python
dataget.vision.mnist(global_cache=True).get()
```

This will download the dataset inside `~/.dataget/{dataset_name}` instead, this is useful if you want to reuse the same dataset across projects. The second is to specify the exact location yourself by using the `path` keyword argument instead:

```python
dataget.vision.mnist(path="/my/dataset/path").get()
```

This gives you full control over the exact location, in this case the dataset will be downloaded `/my/dataset/path`.

## 