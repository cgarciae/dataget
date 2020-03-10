# dataget.structured.movielens_20m
Downloads the [MovieLens 20M](https://grouplens.org/datasets/movielens/20m/) dataset and loads it as `pandas` dataframes.

```python
import dataget

(
    ratings,
    movies,
    tags,
    links,
    genome_scores,
    genome_tags,
) = dataget.structured.movielens_20m().get()
```

## Format
|                   | type         | shape             |
| ----------------- | ------------ | ----------------- |
| **ratings**       | pd.DataFrame | `(20_000_263, 4)` |
| **movies**        | pd.DataFrame | `(27_278, 3)`     |
| **tags**          | pd.DataFrame | `(465_564, 4)`    |
| **links**         | pd.DataFrame | `(27_278, 3)`     |
| **genome_scores** | pd.DataFrame | `(11_709_768, 3)` |
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
* **Folder name**: `structured_movielens_20m`
* **Size on disk**: `836MB`