import dataget

df_train, df_test = dataget.kaggle(dataset="cristiangarcia/pointcloudmnist2d").get(
    files=["train.csv", "test.csv"]
)

print(df_train.shape)
print(df_test.shape)
