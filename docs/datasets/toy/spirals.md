
# dataget.toy.spirals
This is an artificial dataset created using polar functions inspired by a similar dataset found in [tensorflow playground](http://playground.tensorflow.org).

```python
import dataget

df_train, df_test = dataget.toy.spirals().get()
```

## Sample
<img 
    src="https://github.com/colomb-ia/supervised-basico-spirals/raw/master/images/graph.png" 
    alt="spirals-sample" 
    width="80%" 
/>

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