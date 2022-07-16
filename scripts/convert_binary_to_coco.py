"""Script to convert whole object masks into the COCO format"""

import json
from pycocotools import mask
import numpy as np
from PIL import Image
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Metafile paths
BEES_PATH = '../../../data/data_lstudio/Bees_Christian/'
IMAGES_PATH = '../metafiles/Bees_Christian/images.txt'
IMAGES_LABELS_PATH = '../metafiles/Bees_Christian/22_species/image_class_labels.txt'
CLASSES_PATH = '../metafiles/Bees_Christian/22_species/classes.txt'

# Read metafiles into dictionaries
img_dict = mr.metafile_to_dict(IMAGES_PATH)
img_lab_dict = mr.metafile_to_dict(IMAGES_LABELS_PATH)
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

# Define json file for COCO data; it will include lists for categories/classes, images and annotations
coco_json, images, annotations = {}, [], []
categories = [{"id": int(c), "name": cls_dict[c]} for c in cls_dict]
coco_json["categories"] = categories

# Iterate through images and create json entries
threshold = 50  # see ac.rle_to_matrix()
for i in range(1, len(img_dict)):

    file_name, cls_ind = img_dict[str(i)], img_lab_dict[str(i)]
    data = np.array(Image.open(BEES_PATH + file_name))[:, :, 0] # 1st channel is enough

    # Create boolean mask from array (through jpg-interpolation other values other than 0 and 255 are generated)
    data[data <= threshold] = 0  # background
    data[data > threshold]  = 1  # object

    # Compute RLE
    rle = ac.binary_mask_to_rle(data)

    # Calculate area, bbox, height, width
    h, w = rle.get('size')[0], rle.get('size')[1]
    compressed_rle = mask.frPyObjects(rle, h, w)
    area = int(mask.area(compressed_rle))
    bbox = mask.toBbox(compressed_rle).tolist()

    # Create json for COCO
    images.append( {'id': i, 'width': w, 'height': h, 'file_name': file_name} )
    annotations.append( {'segmentation': rle, 'bbox': bbox, 'area': area,
                         'image_id': i, 'category_id': int(cls_ind), 'iscrowd': 0, 'id': i} )

    if i%10 == 0: print(i)

# Add lists of images and annotations to the json
coco_json["images"] = images
coco_json["annotations"] = annotations

annotations_file = '../metafiles/Bees_Christian/22_species/bees_coco.json'
with open(annotations_file, 'w', encoding='utf-8') as f:
    json.dump(coco_json, f, ensure_ascii=True, indent=4)