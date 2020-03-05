
# dataget.vision.cifar10

Downloads the [Cifar 10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset from University of Toronto's website and loads it as `numpy` arrays.

```python
import dataget

X_train, y_train, X_test, y_test = dataget.vision.cifar10().get()
```
## Sample
<img alt="cifar-10-sample" src="https://miro.medium.com/max/944/1*6XQqOifwnmplS22zCRRVaw.png" width="80%" />

## Format

|             | type     | shape                 | dtype |
| ----------- | -------- | --------------------- | ----- |
| **X_train** | np.array | `(50_000, 32, 32, 3)` | uint8 |
| **y_train** | np.array | `(50_000, 1)`         | uint8 |
| **X_test**  | np.array | `(10_000, 32, 32, 3)` | uint8 |
| **y_test**  | np.array | `(10_000, 1)`         | uint8 |

## Info
* **Folder name**: `vision_cifar10`
* **Size on disk**: `178M`
