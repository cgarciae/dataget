# dataget.structured.movielens_latest
Downloads the [MovieLens Latest](https://grouplens.org/datasets/movielens/latest/) dataset and loads it as `pandas` dataframes.
```python
import dataget

(
    ratings,
    movies,
    tags,
    links,
    genome_scores,
    genome_tags,
) = dataget.structured.movielens_latest().get()
```

!!! warning
    This dataset is updates automatically. If you need consistency use `movielens_25m` or `movielens_20m` instead.

## Format
|                   | type         | shape             |
| ----------------- | ------------ | ----------------- |
| **ratings**       | pd.DataFrame | `(27_753_444, 4)` |
| **movies**        | pd.DataFrame | `(58_098, 3)`     |
| **tags**          | pd.DataFrame | `(1_108_997, 4)`  |
| **links**         | pd.DataFrame | `(58_098, 3)`     |
| **genome_scores** | pd.DataFrame | `(14_862_528, 3)` |
| **genome_tags**   | pd.DataFrame | `(1_128, 2)`      |

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
* **Folder name**: `structured_movielens_latest`
* **Size on disk**: `1.2GB`