"""Derive BBoxes out of object masks"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../label_studio_converter')
sys.path.insert(2, '../beexplainable')

import json
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Path to the annotation file exported from Label Studio
ANNOT_PATH = '../../../data/data_lstudio_export/Bees_Christian/wildbees_part_segmentations.json'
# Open json file (needed for heights and widths)
with open(ANNOT_PATH, 'r') as f:
    annot_file = json.load(f)

# Get dictionary with file ids, part ids and RLEs from parts path
PART_LOCS_PATH = '../part_locs.txt'
part_locs_dict = mr.part_locs_to_dict(PART_LOCS_PATH)

# Open new empty file for BBoxes
bbox_file = open("../bounding_boxes.txt", "a")

# Iterate over RLE dict, compute total object masks and derive BBoxes
for annots, file_id in zip(annot_file, part_locs_dict):

    # Annotations are stored under 'result'
    # For each part, h and w are stored again.
    # It is enough to read h and w from the first part annot.
    part_result = annots["annotations"][0]["result"][0]
    h, w = part_result["original_height"], part_result["original_width"]

    # Get segmentation masks for each part
    masks = []
    for part_id in part_locs_dict[file_id]:
        # Convert string RLE arrays to binary matrices
        # Note: The empty string is just a placeholder for the part index.
        #       Since we are not interested in that index here, we do not actually read it
        masks.append( ('', ac.rle_to_matrix(part_locs_dict[file_id][part_id], (h, w))) )

    # Compute total object mask
    obj_mask = ac.union_of_masks(masks)

    # Derive BBox coords. from object mask (in CUB format)
    xmin, ymin, w, h = ac.cub_bbox_from_mask(obj_mask)

    # Write BBox coords. into file
    bbox_file.write(file_id + ' ' + str(xmin) + ' ' + str(ymin) + ' ' +
                    str(w) + ' ' + str(h) + '\n')

bbox_file.close()