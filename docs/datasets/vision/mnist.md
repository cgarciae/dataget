
# dg.vision.mnist

Downloads the [MNIST](http://yann.lecun.com/exdb/mnist/) dataset from Yann LeCun's website and loads it as `numpy` arrays.

```python
import dataget as dg

X_train, y_train, X_test, y_test = dg.vision.mnist().get()
```

## Format

|             | type     | shape             | dtype |
| ----------- | -------- | ----------------- | ----- |
| **X_train** | np.array | `(60000, 28, 28)` | uint8 |
| **y_train** | np.array | `(60000,)`        | uint8 |
| **X_test**  | np.array | `(10000, 28, 28)` | uint8 |
| **y_test**  | np.array | `(10000,)`        | uint8 |

## Info
* **Folder name**: `vision_mnist`
* **Size on disk**: `53MB`
