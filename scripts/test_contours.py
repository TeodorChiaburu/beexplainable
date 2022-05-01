"""Script to test methods of extracting the contour of a binary image"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')
sys.path.insert(2, '../label_studio_converter')

import numpy as np
from PIL import Image
import cv2 as cv
import matplotlib.pyplot as plt
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Pick a file example, and part ID
file_id, part_id = '13', '1'

# Get dictionary of file indexes to file names from images path
IMAGES_PATH = '../metafiles/Bees_Christian/images.txt'
images_dict = mr.metafile_to_dict(IMAGES_PATH)

# Get dictionary with file ids, part ids and RLEs from parts path
PART_LOCS_PATH = '../metafiles/Bees_Christian/part_locs.txt'
part_locs_dict = mr.part_locs_to_dict(PART_LOCS_PATH)

# Find file name in the dictionary and create path to image
im_name = images_dict[file_id]
indiv_name = im_name[: im_name.find('.')] # drop .jpg
BEES_PATH = '../../../data/data_lstudio/Bees_Christian/'
im_path = BEES_PATH + im_name

# Open example image and convert it to np
img = np.array( Image.open(im_path) )
h, w, _ = img.shape

# Convert string RLE arrays to binary matrices
bin_mask = ac.rle_to_matrix(part_locs_dict[file_id][part_id], (h, w))

# Compute edges of mask
# Note: RETR_LIST retrieves all the contours without considering nesting
#       CHAIN_APPROX_NONE stores all contour points, even on straight lines
contours = cv.findContours(bin_mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0]
blank = np.zeros((h, w), dtype = np.uint8)
edges_cv = cv.drawContours(blank, # destination image (NOT source bin_mask!)
                           contours, -1, # -1 means all contours are returned (here only one)
                           color=(255, 255, 255),
                           thickness=10)//255 # thickness a bit higher to enclose the shape
                                              # only for plotting, size of contours not dependent on thickness

refilled = cv.drawContours(blank, contours, -1, color=(255, 255, 255),
                           thickness=-1)//255 # neg. thickness to fill the shape

# Overlay mask on original image and cover up background pixels
overlay = np.copy(img)
overlay[ refilled == 0 ] = np.array([255, 255, 255], dtype = np.uint8)

# Plot results
rows, cols = 2, 3
plt.figure(figsize = (5, 5))
plt.subplot(rows, cols, 1)
plt.imshow(img)
plt.title('Raw')
plt.axis('off')

plt.subplot(rows, cols, 2)
plt.imshow(bin_mask, interpolation='none')
plt.title('Original thorax')
plt.axis('off')

plt.subplot(rows, cols, 3)
plt.imshow(edges_cv, interpolation='none')
plt.title('Contours')
plt.axis('off')

plt.subplot(rows, cols, 5)
plt.imshow(refilled, interpolation='none')
plt.title('Refilling')
plt.axis('off')

plt.subplot(rows, cols, 6)
plt.imshow(overlay, interpolation='none')
plt.title('Overlay')
plt.axis('off')

plt.savefig('../figures/masks_bboxes/Edges_' + indiv_name + '.png', bbox_inches='tight')
plt.show()
