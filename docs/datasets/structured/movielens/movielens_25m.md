
# dataget.structured.movielens_25m
Downloads the [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) dataset and loads it as `pandas` dataframes.

```python
import dataget

(
    ratings,
    movies,
    tags,
    links,
    genome_scores,
    genome_tags,
) = dataget.structured.movielens_25m().get()
```

## Format
|                   | type         | shape             |
| ----------------- | ------------ | ----------------- |
| **ratings**       | pd.DataFrame | `(25_000_095, 4)` |
| **movies**        | pd.DataFrame | `(62_423, 3)`     |
| **tags**          | pd.DataFrame | `(1_093_360, 4)`  |
| **links**         | pd.DataFrame | `(62_423, 3)`     |
| **genome_scores** | pd.DataFrame | `(15_584_448, 3)` |
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
* **Folder name**: `structured_movielens_25m`
* **Size on disk**: `1.1GB`