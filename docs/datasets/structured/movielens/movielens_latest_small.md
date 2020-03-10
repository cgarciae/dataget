# dataget.structured.movielens_latest_small
Downloads the [MovieLens Latest Small](https://grouplens.org/datasets/movielens/latest/) dataset and loads it as `pandas` dataframes.

```python
import dataget

(
    ratings,
    movies,
    tags,
    links,
) = dataget.structured.movielens_latest_small().get()
```

!!! warning
    This dataset is updates automatically. If you need consistency use `movielens_25m` or `movielens_20m` instead.

## Format
|             | type         | shape          |
| ----------- | ------------ | -------------- |
| **ratings** | pd.DataFrame | `(100_836, 4)` |
| **movies**  | pd.DataFrame | `(9_742, 3)`   |
| **tags**    | pd.DataFrame | `(3_683, 4)`   |
| **links**   | pd.DataFrame | `(9_742, 3)`   |

## Features
#### ratings
| column    | type    |
| --------- | ------- |
| userId    | int64   |
| movieId   | int64   |
| rating    | float64 |
| timestamp | int64   |

#### movies
| column  | type   |
| ------- | ------ |
| movieId | int64  |
| title   | object |
| genres  | object |

#### tags
| column  | type    |
| ------- | ------- |
| movieId | int64   |
| imdbId  | int64   |
| tmdbId  | float64 |

#### genome_scores
| column    | type    |
| --------- | ------- |
| movieId   | int64   |
| tagId     | int64   |
| relevance | float64 |

#### genome_tags
| column | type   |
| ------ | ------ |
| tagId  | int64  |
| tag    | object |

## Info
* **Folder name**: `structured_movielens_latest_small`
* **Size on disk**: `3.2MB`