
import os
from sklearn.model_selection import train_test_split
import shutil
import sys


inputpath= sys.argv[2]
outputpath= sys.argv[1]
train_img = os.path.join(outputpath,'images', 'train')
val_img = os.path.join(outputpath,'images', 'val')
train_labels = os.path.join(outputpath,'labels','train')
val_labels = os.path.join(outputpath,'labels','val')
os.makedirs(train_img, exist_ok=True)
os.makedirs(val_img, exist_ok=True)
os.makedirs(train_labels, exist_ok=True)
os.makedirs(val_labels, exist_ok=True)

# Read images and annotations
images = [os.path.join(inputpath,'images', x) for x in os.listdir(os.path.join(inputpath,'images'))]
annotations = [os.path.join(inputpath,'labels', x) for x in os.listdir(os.path.join(inputpath,'labels')) if x[-3:] == "txt"]

images.sort()
annotations.sort()

# Split the dataset into train-valid-test splits 
train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)


#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

# Move the splits into their folders
move_files_to_folder(train_images,train_img)
move_files_to_folder(val_images,val_img)

move_files_to_folder(train_annotations,train_labels)
move_files_to_folder(val_annotations, val_labels)
