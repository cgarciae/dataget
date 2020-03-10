
# dataget.image.fashion_mnist

Downloads the [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) dataset and loads it as `numpy` arrays.

```python
import dataget

X_train, y_train, X_test, y_test = dataget.image.fashion_mnist().get()
```

## Sample
<img 
    src="https://www.researchgate.net/profile/Lina_Yao4/publication/325921786/figure/fig2/AS:640163516522496@1529638284313/Example-for-fashion-MNIST-Each-class-is-represented-by-nine-cases.png" 
    alt="fashion-mnist-sample" 
    width="100%" 
/>

## Format

|             | type     | shape              | dtype |
| ----------- | -------- | ------------------ | ----- |
| **X_train** | np.array | `(60_000, 28, 28)` | uint8 |
| **y_train** | np.array | `(60_000,)`        | uint8 |
| **X_test**  | np.array | `(10_000, 28, 28)` | uint8 |
| **y_test**  | np.array | `(10_000,)`        | uint8 |

## Info
* **Folder name**: `image_fashion_mnist`
* **Size on disk**: `53MB`
