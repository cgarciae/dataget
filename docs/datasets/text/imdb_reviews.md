
# dataget.text.imdb_reviews
Downloads the [IMDB Reviews](http://ai.stanford.edu/~amaas/data/sentiment/) dataset and loads it as `pandas` dataframes.

```python
import dataget

df_train, df_test = dataget.text.imdb_reviews().get()
```
This dataset also contains unsupervised sample, to load them set the `include_unsupervised` argument:

```python
import dataget

df_train, df_test = dataget.text.imdb_reviews().get(include_unsupervised=True)
```
All unsupervised sample will have a label of `-1`. 

## Format
|              | type         | shape         |
| ------------ | ------------ | ------------- |
| **df_train** | pd.DataFrame | `(75_000, 3)` |
| **df_test**  | pd.DataFrame | `(25_000, 3)` |

## Features
| column    | type  |
| --------- | ----- |
| text      | str   |
| label     | int64 |
| text_path | str   |

## Info
* **Folder name**: `text_imdb_reviews`
* **Size on disk**: `490MB`

## API Reference
::: dataget.text.imdb_reviews