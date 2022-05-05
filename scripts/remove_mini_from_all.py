"""Script to remove images from the mini dataset out of the whole dataset"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob, os
from beexplainable.utils import metafile_readers as mr

# Get file names from text file
IMAGES_PATH = "../metafiles/Bees_Christian/images.txt"
imgs_mini = list( mr.metafile_to_dict(IMAGES_PATH).values() )

BEES_PATH = '../../../data/data_lstudio/Bees/'
img_paths = glob.glob(BEES_PATH + '**/*.jpg') # double ** for recursive search (over 30k imgs)

num_deleted = 0
for i in range(len(img_paths)):

    # Get file name (not the whole path) and add it to the dictionary of images
    full_path = img_paths[i]
    file_name = full_path[full_path.rfind('/') + 1:]

    # Remove image from whole dataset if name is found in mini dataset
    if file_name in imgs_mini:
        os.remove(full_path)
        num_deleted += 1
        if num_deleted % 100 == 0 and num_deleted > 0:
            print(f"Deleted {num_deleted} images.")

print(f"Total deleted: {num_deleted}")