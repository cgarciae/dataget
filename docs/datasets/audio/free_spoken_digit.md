
# dataget.audio.free_spoken_digit

Downloads the [Free Spoken Digits](https://github.com/Jakobovski/free-spoken-digit-dataset) dataset and loads its metadata as `pandas` dataframes. The audio samples are as `.wav` files.

```python
import dataget

df = dataget.audio.free_spoken_digit().get()
```
Dataget doesn't load the audio dataset into memory, instead the `df` dataframe has the `audio_path` column which contains the relative path of each `sample`. You can easily load them using [scipy.io.wavfile.read](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.io.wavfile.read.html).

!!! tip
    Its recommended that you split train / test based on `user` instead of randomly to avoid testing based on similar samples found in training.

## Format
|        | type         | shape        |
| ------ | ------------ | ------------ |
| **df** | pd.DataFrame | `(2_000, 4)` |

## Features
| column         | type    | description                                                                                     |
| -------------- | ------- | ----------------------------------------------------------------------------------------------- |
| **audio_path** | `str`   | Relative path of the audio file                                                                 |
| **label**      | `int64` | Target label in the range `[0, 9]`                                                              |
| **user**       | `str`   | Name of the speaker                                                                             |
| **repetition** | `int64` | Repetition number for each (user, label) pair, i.e. each user repeats each digit multiple times |



## Info
* **Folder name**: `audio_free_spoken_digit`
* **Size on disk**: `26MB`
