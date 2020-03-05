
# dataget.vision.mnist

Downloads the [MNIST](http://yann.lecun.com/exdb/mnist/) dataset from Yann LeCun's website and loads it as `numpy` arrays.

```python
import dataget

X_train, y_train, X_test, y_test = dataget.vision.mnist().get()
```

## Sample
<img 
    src="https://www.researchgate.net/profile/Vassili_Kovalev/publication/302955130/figure/fig1/AS:360822447591424@1463038183819/Examples-of-MNIST-digit-images.png" 
    alt="mnist-sample" 
    width="80%" 
/>

## Format

|             | type     | shape              | dtype |
| ----------- | -------- | ------------------ | ----- |
| **X_train** | np.array | `(50_000, 28, 28)` | uint8 |
| **y_train** | np.array | `(50_000,)`        | uint8 |
| **X_test**  | np.array | `(10_000, 28, 28)` | uint8 |
| **y_test**  | np.array | `(10_000,)`        | uint8 |

## Info
* **Folder name**: `vision_mnist`
* **Size on disk**: `53MB`
