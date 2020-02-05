import dataget as dg

X_train, y_train, X_test, y_test = dg.data.vision.mnist().get()

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)
