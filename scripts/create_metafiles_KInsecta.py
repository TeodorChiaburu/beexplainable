"""Create images.txt and images_labels.txt for KInsecta"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob
from beexplainable.utils import metafile_readers as mr

# Metafile folder
bees_folder = "../metafiles/KInsecta/"
#subfolder   = "full_images_ilona/"
subfolder   = "ilona_squared/"

# Read class names
CLASSES_PATH = bees_folder + subfolder + "classes.txt"
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

images = open(bees_folder + subfolder + "images_validation.txt", "a")
image_class_labels = open(bees_folder + subfolder + "image_class_labels_validation.txt", "a")

# Get all paths to the bees
BEES_PATH = '../../../data/KInsecta_webapp_data_2022_09_02/' + subfolder + 'validation/'
img_paths = glob.glob(BEES_PATH + '*/*.png')

for i in range(len(img_paths)):

    # Get file name and discard the common main path
    # Note: you are left with species_folder/file_name.png
    file_name = img_paths[i][len(BEES_PATH):]

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