import os
from PIL import Image

dataset_path = "train_dir"

for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)

    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            try:
                img = Image.open(file_path)
                img.verify()
            except:
                print("Removing corrupted:", file_path)
                os.remove(file_path)

print("Dataset cleaned successfully!")