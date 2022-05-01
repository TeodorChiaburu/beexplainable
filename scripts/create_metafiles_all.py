"""Create metafiles for the whole downloaded wildbee dataset (formats inspired by CUB200)"""
"""Only images.txt and images_labels.txt are created here"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob
from beexplainable.utils import metafile_readers as mr

# Read class names
CLASSES_PATH = "../metafiles/classes.txt"
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

images = open("../metafiles/Bees/images.txt", "a")
image_class_labels = open("../metafiles/Bees/image_class_labels.txt", "a")

BEES_PATH = '../../../data/data_lstudio/Bees/'
img_paths = glob.glob(BEES_PATH + '**/*.jpg') # double ** for recursive search (over 30k imgs)

for i in range(len(img_paths)):

    # Get file name (not the whole path) and add it to the dictionary of images
    file_name = img_paths[i]
    file_name = file_name[file_name.rfind('/') + 1:]
    images.write(str(i+1) + ' ' + file_name + '\n')

    # Infer class from file name
    substrs = file_name.split('_')
    cls = substrs[0] + '_' + substrs[1]

    # Get class index from its name and write the pair (file_id, cls_id) to file
    cls_ind = list(cls_dict.keys())[list(cls_dict.values()).index(cls)]
    image_class_labels.write(str(i+1) + ' ' + str(cls_ind) + '\n')

    if i % 1000 == 0: print(i)

images.close()
image_class_labels.close()