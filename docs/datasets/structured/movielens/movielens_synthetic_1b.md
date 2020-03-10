# dataget.structured.movielens_synthetic_1b
Downloads the [MovieLens Synthetic 1B](https://grouplens.org/datasets/movielens/movielens-1b/) dataset returns an iterable of numpy `numpy` arrays.
```python
import dataget

ratings_iterable = dataget.structured.movielens_synthetic_1b().get()
```
By default each array has a different length (the dataset is organized like this), to make training easier we provide the `batch_size` keyword argument which you can use to get arrays of a given length. 

```python
import dataget

ratings_iterable = dataget.structured.movielens_synthetic_1b().get(batch_size=64)
```

!!! note
    Depending of the `batch_size` the last array may have a smaller size than the rest.

If you have enough memory you can consider concatenating all into a single array:
```python
import dataget

ratings_iterable = dataget.structured.movielens_synthetic_1b().get()
ratings = np.concatenate(ratings_iterable, axis=0)
```

## Format
|                      | type               | full shape           | dtype |
| -------------------- | ------------------ | -------------------- | ----- |
| **ratings_iterable** | Iterable[np.array] | `(1_226_159_268, 2)` | int64 |

## Features
| column | description | total       |
| ------ | ----------- | ----------- |
| `0`    | users       | `22_10_078` |
| `1`    | movies      | `855_776`   |


## Info
* **Folder name**: `structured_movielens_synthetic_1b`
* **Size on disk**: `3.1GB`