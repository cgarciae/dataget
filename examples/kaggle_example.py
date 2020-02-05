import dataget as dg

df_train, df_test = dg.data.kaggle("cristiangarcia/pointcloudmnist2d").get(
    files=["train.csv", "test.csv"]
)

print(df_train.shape)
print(df_test.shape)
