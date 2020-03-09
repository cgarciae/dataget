
# dataget.vision.imagenet

Downloads the [ImageNet](https://www.kaggle.com/c/imagenet-object-localization-challenge) dataset from their official ImageNet Object Localization Challenge Kaggle competition and loads its metadata as `pandas` dataframes. You need the `kaggle` cli installed and configured to use this dataset.

```python
import dataget

df_train, df_val, df_test = dataget.vision.imagenet().get()
```
Dataget doesn't load the images of this dataset into memory, instead the `df_train`, `df_val`, and `df_test` dataframes contain the `image_path` column which contains the relative path of each sample which you can latter use to iteratively load each image during training.

## Sample
<img 
    src="https://www.researchgate.net/profile/Yuzhuo_Ren/publication/314646236/figure/fig7/AS:668983594336276@1536509526997/Examples-in-the-ImageNet-dataset.png" 
    alt="imagenet-sample" 
    width="100%" 
/>

## Format

|              | type         | shape           |
| ------------ | ------------ | --------------- |
| **df_train** | pd.DataFrame | `(544_546, 10)` |
| **df_val**   | pd.DataFrame | `(50_000, 9)`   |
| **df_test**  | pd.DataFrame | `(100000, 2)`   |

## Features
#### df_train
| column           | type  | description                |
| ---------------- | ----- | -------------------------- |
| image_path       | str   | relative path of the image |
| label            | str   | label id                   |
| xmin             | int64 | bouding box annotation     |
| ymin             | int64 | bouding box annotation     |
| xmax             | int64 | bouding box annotation     |
| ymax             | int64 | bouding box annotation     |
| label_name       | str   | full label name            |
| wnid             | str   | wnid                       |
| ImageId          | str   | image id                   |
| PredictionString | str   | full prediction string     |

#### df_val
| column           | type  | description                |
| ---------------- | ----- | -------------------------- |
| image_path       | str   | relative path of the image |
| label            | str   | label id                   |
| xmin             | int64 | bouding box annotation     |
| ymin             | int64 | bouding box annotation     |
| xmax             | int64 | bouding box annotation     |
| ymax             | int64 | bouding box annotation     |
| label_name       | str   | full label name            |
| ImageId          | str   | image id                   |
| PredictionString | str   | full prediction string     |

#### df_test
| column     | type | description                |
| ---------- | ---- | -------------------------- |
| image_path | str  | relative path of the image |
| ImageId    | str  | image id                   |


## Info
* **Folder name**: `vision_imagenet`
* **Size on disk**: `161GB`
