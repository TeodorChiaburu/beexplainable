"""Derive BBoxes out of object masks"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../label_studio_converter')
sys.path.insert(2, '../beexplainable')

import json
import numpy as np
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Path to the annotation file exported from Label Studio
#ANNOT_PATH = '../../../data/data_lstudio_export/Bees_Christian/wildbees_part_segmentations.json'
# Open json file (needed for heights and widths)
#with open(ANNOT_PATH, 'r') as f:
    #annot_file = json.load(f)

# Get dictionary with file ids, part ids and RLEs from parts path
PART_LOCS_PATH = '../metafiles/part_locs.txt'
part_locs_dict = mr.part_locs_to_dict(PART_LOCS_PATH)

# Open new empty file for BBoxes
bbox_file = open("../metafiles/bounding_boxes.txt", "a")

# Get dictionary with file ids and w-h-tuples
W_H_PATH = '../metafiles/widths_heights.txt'
w_h_dict = mr.w_h_to_dict(W_H_PATH)

# Open new empty file for binary masks
#bin_mask_file = open("../metafiles/binary_masks.txt", "a")

# Iterate over RLE dict, compute total object masks and derive BBoxes
for file_id in part_locs_dict:

    # Annotations are stored under 'result'
    # For each part, h and w are stored again.
    # It is enough to read h and w from the first part annot.
    #part_result = annots["annotations"][0]["result"][0]
    #h, w = part_result["original_height"], part_result["original_width"]

    # Get w-h-tuple from dictionary
    w, h = w_h_dict[file_id]

    # Get segmentation masks for each part
    masks = []
    for part_id in part_locs_dict[file_id]:
        # Convert string RLE arrays to binary matrices
        bin_mask = ac.rle_to_matrix(part_locs_dict[file_id][part_id], (int(h), int(w)))

        # Get 1D indexes of the 1's in the binary mask
        #mask_ind = ac.binary_mask_to_indexes(bin_mask, output_as_strings = True)

        # Store the indexes in a string chain with white spaces in between
        #mask_ind_str = ' '.join(mask_ind)

        # Write indexes of masked pixels to file
        #bin_mask_file.write(file_id + ' ' + part_id + ' ' + mask_ind_str + '\n')

        # Note: The empty string is just a placeholder for the part index.
        #       Since we are not interested in that index here, we do not actually read it (empty string instead)
        masks.append( ('', bin_mask) )

    # Compute total object mask
    obj_mask = ac.union_of_masks(masks)
    # Get 1D indexes of the 1's in the binary mask
    #mask_ind = ac.binary_mask_to_indexes(obj_mask, output_as_strings=True)
    # Store the indexes in a string chain with white spaces in between
    #mask_ind_str = ' '.join(mask_ind)
    # Write indexes of masked pixels to file (part index 0 marks the mask coordinates for the whole object)
    #bin_mask_file.write(file_id + ' 0 ' + mask_ind_str + '\n')

    # Derive BBox coords. from object mask (in CUB format)
    xmin, ymin, w, h = ac.cub_bbox_from_mask(obj_mask)

    # Write BBox coords. into file
    bbox_file.write(file_id + ' ' + str(xmin) + ' ' + str(ymin) + ' ' +
                    str(w) + ' ' + str(h) + '\n')

bbox_file.close()
#bin_mask_file.close()