
# dataget.vision.imagenet

Downloads the [ImageNet](https://www.kaggle.com/c/imagenet-object-localization-challenge) dataset from their official **ImageNet Object Localization Challenge** Kaggle competition and loads its metadata as `pandas` dataframes. You need the [Kaggle CLI](https://github.com/Kaggle/kaggle-api) installed and configured to use this dataset.

```python
import dataget

df_train, df_val, df_test = dataget.vision.imagenet().get()
```
Dataget doesn't load the images of this dataset into memory, instead the `df_train`, `df_val`, and `df_test` dataframes has the `image_path` column which contains the relative path of each sample which you can latter use to iteratively load each image during training.

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
| **df_test**  | pd.DataFrame | `(100_000, 2)`  |

## Features
| column           | type  | description                                     | df_train | df_val | df_test |
| ---------------- | ----- | ----------------------------------------------- | :------: | :----: | :-----: |
| ImageId          | str   | image id                                        |  **x**   | **x**  |  **x**  |
| image_path       | str   | relative path to jpeg image                     |  **x**   | **x**  |  **x**  |
| annotations_path | str   | relative path to pascal voc xml                 |  **x**   | **x**  |         |
| label            | str   | label id                                        |  **x**   | **x**  |         |
| label_name       | str   | label name                                      |  **x**   | **x**  |         |
| PredictionString | str   | prediction string                               |  **x**   | **x**  |         |
| xmin             | int64 | prediction string bouding box coord             |  **x**   | **x**  |         |
| ymin             | int64 | prediction string bouding box coord             |  **x**   | **x**  |         |
| xmax             | int64 | prediction string bouding box coord             |  **x**   | **x**  |         |
| ymax             | int64 | prediction string bouding box coord             |  **x**   | **x**  |         |
| wnid             | str   | [WordNet ID](http://image-net.org/download-API) |  **x**   |        |         |



## Info
* **Folder name**: `vision_imagenet`
* **Size on disk**: `161GB`
