
# Spirals Challenge
## Description
This is an artificial set created using polar functions inspired by a similar one found in [tensorflow playground](http://playground.tensorflow.org).

![graph](https://github.com/colomb-ia/supervised-basico-spirals/raw/master/images/graph.png)

## Example
```python
import dataget

df_train, df_test = dataget.toy.spirals().get()
```

## Format

|              | type         | shape      |
| ------------ | ------------ | ---------- |
| **df_train** | pd.DataFrame | `(399, 3)` |
| **df_test**  | pd.DataFrame | `(45, 3)`  |

## Features

| x0    | x1    | y   |
| ----- | ----- | --- |
| float | float | int |

## Info
* **Folder name**: `toy_spirals`
* **Size on disk**: `24KB`