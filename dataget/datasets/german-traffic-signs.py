# import urllib
# import zipfile
# import os
# import shutil
# from dataget.utils import get_file
# from dataget.dataset import ImageDataSetWithMetadata
# from dataget.api import register_dataset
# from multiprocessing import Pool
# from dataget.utils import OS_SPLITTER

# TRAINING_SET_URL = "http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Training_Images.zip"
# TEST_SET_URL = "http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_Images.zip"
# TEST_CSV_URL = "http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_GT.zip"

# @register_dataset
# class GermanTrafficSigns(ImageDataSetWithMetadata):

#     def __init__(self, *args, **kwargs):
#         super(GermanTrafficSigns, self).__init__(*args, **kwargs)

#         self._training_images_path = os.path.join(self.training_set.path, "GTSRB/Final_Training/Images")
#         self._test_images_path = os.path.join(self.test_set.path, "GTSRB/Final_Test/Images")


#     @property
#     def _raw_extension(self):
#         return "ppm"

#     @property
#     def help(self):
#         return "TODO"

#     def reqs(self, **kwargs):
#         return super(GermanTrafficSigns, self).reqs() + ""


#     def _download(self, **kwargs):
#         get_file(TRAINING_SET_URL, self.path, "training-set.zip")
#         get_file(TEST_CSV_URL, self.path, "test-set.csv.zip")
#         get_file(TEST_SET_URL, self.path, "test-set.zip")

#     def _extract_training_set(self, **kwargs):
#         import pandas as pd

#         print("extracting training-set.zip")
#         with zipfile.ZipFile(os.path.join(self.path, "training-set.zip"), 'r') as zip_ref:
#             for file in zip_ref.namelist():


#                 # skip directories
#                 if os.path.basename(file):

#                     if file.endswith(".csv") or file.endswith(self.raw_extension):
#                         # print(file)
#                         # print(self.path)
#                         # os.path.join(self.path, file) |> print
#                         structure = file |> .split("/")
#                         filename = structure[-1]
#                         class_id = structure[-2] |> int |> str


#                         if not os.path.join(self.training_set.path, class_id) |> os.path.exists:
#                             os.path.join(self.training_set.path, class_id) |> os.makedirs

#                         if file.endswith(".csv"):
#                             filename = "{}.csv".format(class_id)


#                         # copy file (taken from zipfile's extract)
#                         path = os.path.join(self.training_set.path, class_id, filename)
#                         source = zip_ref.open(file)
#                         target = open(path, "wb")

#                         with source, target:
#                             shutil.copyfileobj(source, target)

#                         if file.endswith(".csv"):
#                             df = pd.read_csv(path, sep=";")
#                             df.columns = df.columns |> map$(.lower()) |> list
#                             df.rename(columns={'classid':'class_id'}, inplace=True)
#                             df.to_csv(path, index=False)



#     def _extract_test_set(self, **kwargs):
#         print("extracting test-set.zip")
#         with zipfile.ZipFile(os.path.join(self.path, "test-set.zip"), 'r') as zip_ref:
#             for file in zip_ref.namelist():
#                 # skip directories
#                 if os.path.basename(file):

#                     if file.endswith(self.raw_extension):
#                         structure = file |> .split("/")
#                         filename = structure[-1]
#                         path = os.path.join(self.test_set.path, filename)

#                         # copy file (taken from zipfile's extract)
#                         source = zip_ref.open(file)
#                         target = open(path, "wb")

#                         with source, target:
#                             shutil.copyfileobj(source, target)

#         print("extracting test-set.csv.zip")
#         with os.path.join(self.path, "test-set.csv.zip") |> zipfile.ZipFile$(?, 'r') as zip_ref:
#             path = os.path.join(self.test_set.path, "test-set.csv")

#             # copy file (taken from zipfile's extract)
#             source = zip_ref.open("GT-final_test.csv")
#             target = open(path, "wb")

#             with source, target:
#                 shutil.copyfileobj(source, target)

#             with os.path.join(self.test_set.path, "test-set.csv") |> open$(?, "r") as f:
#                 txt = f.read().replace(";", ",")

#             with os.path.join(self.test_set.path, "test-set.csv") |> open$(?, "w") as f:
#                 f.write(txt)



#         self._structure_folder_from_csv(self.test_set.path)

#         #remove old csv
#         os.path.join(self.test_set.path, "test-set.csv") |> os.remove


#     def _structure_folder_from_csv(self, dir_path):
#         import pandas as pd

#         print("organizing test-set")

#         csv_files = os.listdir(dir_path) |> filter$(.endswith(".csv")) |> map$(os.path.join$(dir_path))

#         df = csv_files |> map$(pd.read_csv) |> pd.concat
#         df.columns = df.columns |> map$(.lower()) |> list
#         df.rename(columns={'classid':'class_id'}, inplace=True)

#         groups = df.groupby(["class_id"])

#         for class_id, group in groups:
#             group = group.copy()
#             class_path = os.path.join(dir_path, str(class_id))
#             group_csv_path = os.path.join(class_path, str(class_id)) + ".csv"

#             for i, row in group.iterrows():
#                 file_path = os.path.join(class_path, row.filename)
#                 current_file_path = os.path.join(dir_path, row.filename)

#                 if not os.path.exists(class_path):
#                     os.makedirs(class_path)

#                 # move files
#                 os.rename(current_file_path, file_path)


#             #create group csv
#             group.to_csv(group_csv_path, index=False)



#     def _extract(self, **kwargs):
#         self._extract_training_set(**kwargs)
#         self._extract_test_set(**kwargs)


#     def process_dataframe(self, dataframe, **kwargs):
#         # print(dataframe.iloc[0].class_id)
#         pass
