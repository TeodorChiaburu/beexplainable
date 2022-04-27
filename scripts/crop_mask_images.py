"""Script to generate additional datasets of bbox-cropped images, masked ones and both"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')
sys.path.insert(2, '../label_studio_converter')

import numpy as np
from beexplainable.utils import annot_computers as ac # an extra prefix beexplainable. may be needed
from beexplainable.utils import metafile_readers as mr
from beexplainable.modelling import classifiers as cls
from beexplainable.preprocessing import parsers as ps

# Metafile paths
BEES_PATH = '../data/data_lstudio/Bees_Christian/'
BEES_PATH_BBOX = '../data/data_lstudio/Bees_Christian_bbox/'
IMAGES_PATH = './beexplainable/metafiles/images.txt'
W_H_PATH = './beexplainable/metafiles/widths_heights.txt'
IMAGES_LABELS_PATH = './beexplainable/metafiles/image_class_labels.txt'
CLASSES_PATH = './beexplainable/metafiles/classes.txt'
MODELS_PATH = './beexplainable/models/'
BBOX_PATH = './beexplainable/metafiles/bounding_boxes.txt'
PART_CONTOURS = './beexplainable/metafiles/part_contours.npy'

# Read images and metafiles
img_dict  = mr.metafile_to_dict(IMAGES_PATH)
bbox_dict = mr.bboxes_to_dict(BBOX_PATH, values_as_strings = True)
w_h_dict = mr.w_h_to_dict(W_H_PATH)
with open(PART_CONTOURS, "rb") as f:
    contours = np.load(f, allow_pickle=True)

### 1. Crop images to bounding boxes and store them in a separate folder
ps.parse_image_bbox(img_dict, bbox_dict, src = BEES_PATH, target = BEES_PATH_BBOX)


