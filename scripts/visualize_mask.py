"""Visualize body part masks"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../label_studio_converter')
sys.path.insert(2, '../beexplainable')

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from label_studio_converter.brush import decode_rle
from beexplainable import metafile_readers as mr

IMAGES_PATH = '../images.txt'
PARTS_PATH = '../parts.txt'
PART_LOCS_PATH = '../part_locs.txt'
BEES_PATH = '../../../data/data_lstudio/Bees_Christian/'

# Get dictionary of file indexes to file names from images path
images_dict = mr.metafile_to_dict(IMAGES_PATH)

# Pick an example image (ids start from 1)
im_id = 300

# Find file name in the dictionary and create path to image
im_name = images_dict[str(im_id)]
indiv_name = im_name[: im_name.find('.')] # drop .jpg
im_path = BEES_PATH + im_name

# Open example image and convert it to np
im = np.array( Image.open(im_path) )
h, w, _ = im.shape

# Get dictionary with part ids and part names
parts_dict = mr.metafile_to_dict(PARTS_PATH)

# Get dictionary with file ids, part ids and RLEs from parts path
part_locs_dict = mr.part_locs_to_dict(PART_LOCS_PATH)

# Get RLEs for the chosen image
ex_part_locs = part_locs_dict[str(im_id)]

# Decode the RLE lists into a segmentation masks for each body part
masks = [] # will be a list of tuples (part_name, mask_matrix)
for part_id in ex_part_locs:
    mask = decode_rle(ex_part_locs[part_id]) # 1d array
    mask = np.reshape(mask, (h, w, 4)) # h, w, 4 channels for colors and alpha
    masks.append( (parts_dict[part_id], (mask[:, :, 0])) )# 1st channel is enough (it is only a matrix of 0s and 1s)

# Plot masks
fig = plt.figure(figsize = (10, 8))
fig.suptitle(indiv_name, fontsize = 15)
for i in range(len(masks)):
    # Plot white mask on black background
    plt.subplot(2, 3, i+1)
    plt.imshow(masks[i][1])
    plt.title(masks[i][0])
    plt.axis('off')

    # Plot mask overlaid on image
    masked = np.ma.masked_where(masks[i][1] == 0, masks[i][1])
    plt.subplot(2, 3, i+4)
    plt.imshow(im, interpolation='none')
    plt.imshow(masked, 'jet', interpolation='none', alpha=0.7)
    plt.axis('off')
plt.savefig('Masks_' + indiv_name + '.png', bbox_inches='tight')
plt.show()