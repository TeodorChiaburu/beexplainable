"""Script to split annotated images into training and validation sets (needed to train YOLO)"""

import shutil
from beexplainable.utils import metafile_readers as mr

# Data and metafile paths
BEES_PATH  = '../../../data/data_lstudio/Bees_Christian_masked_bbox/Whole/'
TRAIN_PATH = '../../../data/data_lstudio/Bees_Christian_masked_bbox_train/'
VAL_PATH   = '../../../data/data_lstudio/Bees_Christian_masked_bbox_val/'
IMAGES_PATH = '../metafiles/Bees_Christian/images.txt'

# Read metafiles into dictionary
img_dict = mr.metafile_to_dict(IMAGES_PATH)

num_train = 500 # same as in convert_whole_binary_to_coco.py
for i in range(1, len(img_dict)+1):
    file_name = img_dict[str(i)]
    if i <= num_train:
        shutil.copy(BEES_PATH + file_name, TRAIN_PATH + file_name)
    else:
        shutil.copy(BEES_PATH + file_name, VAL_PATH + file_name)