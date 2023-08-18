"""Crop images segmented with MaskRCNN down to the bounding box"""

import glob
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from beexplainable.utils import annot_computers as ac

SOURCE_PATH = '../../../data/Wildbienen/Bees_masked/'
TARGET_PATH = '../../../data/Wildbienen/Bees_masked_bbox/'
spec_folders = glob.glob(SOURCE_PATH + '*')

# Create analogous empty folders
# for sf in spec_folders:
#     sf = sf[len(SOURCE_PATH):]
#     os.mkdir(TARGET_PATH + sf)

thresh = 255 # for the white in the background
for sf in spec_folders:
    spec_files = glob.glob(sf + '/*.jpg')

    for f in spec_files:
        im = Image.open(f)
        im_gray = np.array( im.convert('L') ) # gray scale
        im_bin = (im_gray < thresh) * 1 # binarize (1 for mask, 0 for background)

        # Derive BBox coords. from object mask (in CUB format)
        xmin, ymin, w, h = ac.cub_bbox_from_mask(im_bin)

        f_target = f.replace('masked', 'masked_bbox')
        plt.imsave( f_target, np.array(im)[int(ymin):int(ymin+h), int(xmin):int(xmin+w), :] )

    print(sf)
print('DONE')