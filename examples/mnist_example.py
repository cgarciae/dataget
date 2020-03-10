import dataget

X_train, y_train, X_test, y_test = dataget.image.mnist().get()

print(X_train.shape, X_train.dtype)
print(y_train.shape, y_train.dtype)
print(X_test.shape, X_test.dtype)
print(y_test.shape, y_test.dtype)
