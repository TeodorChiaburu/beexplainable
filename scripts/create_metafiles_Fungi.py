"""Create images.txt and images_labels.txt for Danish Fungi"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob
from beexplainable.utils import metafile_readers as mr

# Metafile folder
fungi_folder = "../metafiles/Fungi/masked/"

# Read class names
CLASSES_PATH = fungi_folder + "classes.txt"
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

images = open(fungi_folder + "images.txt", "a")
image_class_labels = open(fungi_folder + "image_class_labels.txt", "a")

# Get all paths to the images
FUNGI_PATH = '../../../data/DanishFungi/DF20M_3spec_masked/'
img_paths = glob.glob(FUNGI_PATH + '*/*.JPG')

for i in range(len(img_paths)):

    # Get file name and discard the common main path
    # Note: you are left with species_folder/file_name.jpg
    file_name = img_paths[i][len(FUNGI_PATH):]

    # Infer class from file name
    cls = file_name.split('/')[0]

    # Images are stored in extra species subfolders
    images.write(str(i + 1) + ' ' + file_name + '\n')

    # Get class index from its name and write the pair (file_id, cls_id) to file
    cls_ind = list(cls_dict.keys())[list(cls_dict.values()).index(cls)]
    image_class_labels.write(str(i+1) + ' ' + str(cls_ind) + '\n')

    if i % 100 == 0: print(i)

images.close()
image_class_labels.close()