"""Script to split images cropped by MaskRCNN into train and split (needed by ProtoTree)"""

import shutil, glob
from beexplainable.utils import metafile_readers as mr

# Data and metafile paths
BEES_PATH = '../../../data/data_lstudio/Bees_bbox/'
VAL_PATH  = '../../../data/data_lstudio/Bees_bbox_val/'
CLS_PATH  = '../metafiles/Bees/masked/22_species/classes.txt'

# Get classes
classes = mr.metafile_to_dict(CLS_PATH).values()

percent_val = 0.33

for c in classes:
    total_imgs = glob.glob(BEES_PATH + c + '/*.jpg')
    num_val = int(len(total_imgs) * 0.33)

    # Cut and paste images to the val. folder
    for i in range(num_val):
        val_img = total_imgs[i]
        file_name = val_img[ val_img.rfind('/') : ] # name including backslash
        shutil.move(val_img, VAL_PATH + c + file_name)

    print(c + ' finished.')