"""Script to generate additional datasets of bbox-cropped images, masked ones and both"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')
sys.path.insert(2, '../label_studio_converter')

import numpy as np
from beexplainable.utils import metafile_readers as mr
from beexplainable.preprocessing import dataset_transformers as dt

# Metafile paths
BEES_PATH = '../../../data/data_lstudio/Bees_Christian/'
BEES_PATH_BBOX = '../../../data/data_lstudio/Bees_Christian_bbox/'
BEES_PATH_MASKED = '../../../data/data_lstudio/Bees_Christian_masked/'
BEES_PATH_MASKED_WHOLE = '../../../data/data_lstudio/Bees_Christian_masked/Whole/'
BEES_PATH_MASKED_BBOX = '../../../data/data_lstudio/Bees_Christian_masked_bbox/'
BEES_PATH_MASKS = '../../../data/data_lstudio/Bees_Christian_masks/'
BEES_PATH_MASKS_WHOLE = '../../../data/data_lstudio/Bees_Christian_masks/Whole/'
IMAGES_PATH = '../metafiles/Bees_Christian/images.txt'
W_H_PATH = '../metafiles/Bees_Christian/widths_heights.txt'
BBOX_PATH = '../metafiles/Bees_Christian/bounding_boxes.txt'
PARTS_PATH = '../metafiles/Bees_Christian/parts.txt'
PART_CONTOURS = '../metafiles/Bees_Christian/part_contours.npy'

# Read images and metafiles
img_dict  = mr.metafile_to_dict(IMAGES_PATH)
parts_dict = mr.metafile_to_dict(PARTS_PATH)
bbox_dict = mr.bboxes_to_dict(BBOX_PATH, values_as_strings = False)
w_h_dict = mr.w_h_to_dict(W_H_PATH)
with open(PART_CONTOURS, "rb") as f:
    contours = np.load(f, allow_pickle=True)

### 1. Crop images to bounding boxes and store them in a separate folder
dt.crop_images_to_bbox(img_dict, bbox_dict, src=BEES_PATH, target=BEES_PATH_BBOX)
print('BBox finished')

### 2. Mask body parts in images and store results in a separate folder
dt.mask_body_parts(img_dict, contours, w_h_dict, parts_dict, src = BEES_PATH,
                   target_overlay = BEES_PATH_MASKED, target_mask = BEES_PATH_MASKS)
print('Masked parts finished')

### 3. Mask whole objects and store results in a separate folder
dt.mask_whole_object(img_dict, contours, w_h_dict, parts_dict, src = BEES_PATH,
                     target_overlay = BEES_PATH_MASKED_WHOLE, target_mask = BEES_PATH_MASKS_WHOLE)
print('Masked whole object finished')

### 4. Mask whole objects, then crop to bbox and store results in a separate folder
dt.mask_whole_object(img_dict, contours, w_h_dict, parts_dict, src = BEES_PATH,
                     target_overlay = BEES_PATH_MASKED_BBOX, bbox_dict = bbox_dict)
print('BBox and masked whole object finished')