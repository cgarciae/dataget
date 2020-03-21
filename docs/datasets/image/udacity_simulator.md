
# dataget.image.udacity_simulator

Downloads the [Udacity Simulator](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584f6edd_data/data.zip) dataset and loads it as `pandas` dataframes. Images are not loaded into memory but the `center`, `left`, and `right` column contain the relative path to their files.

```python
import dataget

df = dataget.image.udacity_simulator().get()
```

Do not use random shuffling to spit the data as similar images from the training set will appear on the test set.

## Sample
<img 
    src="https://tomaszkacmajor.pl/wp-content/uploads/2018/05/image_examples.jpg" 
    alt="simulator-sample" 
    width="100%" 
/>

## Format

|        | type         | shape       |
| ------ | ------------ | ----------- |
| **df** | pd.DataFrame | `(8036, 7)` |


## Features
| column   | type    | description                                    |
| -------- | ------- | ---------------------------------------------- |
| center   | str     | relative path of the center camera `jpg` image |
| left     | str     | relative path of the left camera `jpg` image   |
| right    | str     | relative path of the right camera `jpg` image  |
| steering | float64 | stearing angle                                 |
| throttle | float64 | throttle magnitude                             |
| brake    | float64 | break mangnitude                               |
| speed    | float64 | speed mangnitude                               |



## Info
* **Folder name**: `image_udacity_simulator`
* **Size on disk**: `465MB`
