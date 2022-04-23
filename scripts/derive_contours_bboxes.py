"""Derive BBoxes out of object masks"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../label_studio_converter')
sys.path.insert(2, '../beexplainable')

import cv2 as cv
import numpy as np
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Get dictionary with file ids, part ids and RLEs from parts path
PART_LOCS_PATH = '../metafiles/part_locs.txt'
part_locs_dict = mr.part_locs_to_dict(PART_LOCS_PATH)

# Open new empty file for BBoxes
bbox_file = open("../metafiles/bounding_boxes.txt", "a")

# Get dictionary with file ids and w-h-tuples
W_H_PATH = '../metafiles/widths_heights.txt'
w_h_dict = mr.w_h_to_dict(W_H_PATH)

# Open new empty file for binary masks
contour_file = open("../metafiles/part_contours.npy", "wb")

# Iterate over RLE dict, compute total object masks and derive BBoxes
contours = []
for file_id in part_locs_dict:

    # Get w-h-tuple from dictionary
    w, h = w_h_dict[file_id]

    # Get segmentation masks for each part
    masks = []
    for part_id in part_locs_dict[file_id]:
        # Convert string RLE arrays to binary matrices
        bin_mask = ac.rle_to_matrix(part_locs_dict[file_id][part_id], (int(h), int(w)))

        # Find contour of binary mask (see test_contours.py)
        contour = cv.findContours(bin_mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0][0]

        # Prepend file_id and part_id to the contour array
        contour = np.insert(contour, 0, [[int(file_id), int(part_id)]], axis=0)
        contours.append(contour)

        # Note: The empty string is just a placeholder for the part index.
        #       Since we are not interested in that index here, we do not actually read it (empty string instead)
        masks.append( ('', bin_mask) )

    # Compute total object mask
    obj_mask = ac.union_of_masks(masks)

    # Derive BBox coords. from object mask (in CUB format)
    xmin, ymin, w, h = ac.cub_bbox_from_mask(obj_mask)

    # Write BBox coords. into file
    bbox_file.write(file_id + ' ' + str(xmin) + ' ' + str(ymin) + ' ' +
                    str(w) + ' ' + str(h) + '\n')

    # Print progress
    if int(file_id) % 10 == 0:
        print(file_id)

# Store the whole list of contours into a numpy file
np.save(contour_file, np.asarray(contours))

bbox_file.close()
contour_file.close()