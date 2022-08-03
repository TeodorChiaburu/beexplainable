"""Script to convert whole object masks into the COCO format"""

import json
from pycocotools import mask
import numpy as np
from PIL import Image
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Metafile paths
BEES_PATH = '../../../data/data_lstudio/Bees_Christian_masks/Whole/'
IMAGES_PATH = '../metafiles/Bees_Christian/images.txt'
IMAGES_LABELS_PATH = '../metafiles/Bees_Christian/22_species/image_class_labels.txt'
CLASSES_PATH = '../metafiles/Bees_Christian/22_species/classes.txt'
BBOX_PATH = '../metafiles/Bees_Christian/bounding_boxes.txt'

# Whether to classify objects as 'Insects' or concrete genus_species
ONE_CLASS = True

# Read metafiles into dictionary
img_dict = mr.metafile_to_dict(IMAGES_PATH)
img_lab_dict = mr.metafile_to_dict(IMAGES_LABELS_PATH)
cls_dict = mr.metafile_to_dict(CLASSES_PATH)
bbox_dict = mr.bboxes_to_dict(BBOX_PATH, values_as_strings = False)

# Define json file for COCO data; it will include lists for categories/classes, images and annotations
coco_json_train, coco_json_val = {}, {}
images, annotations = [], []
# Note: the json files will be used in the detectron2 library, which requires classes to start at index 0!
if ONE_CLASS:
    categories = [{"id": 0, "name": "Insect"}]
else:
    categories = [{"id": int(c)-1, "name": cls_dict[c]} for c in cls_dict]
coco_json_train["categories"] = coco_json_val["categories"] = categories

# Iterate through images and create json entries
threshold = 50  # see ac.rle_to_matrix()
num_train = 500 # how many images should go into the json used for training
for i in range(1, len(img_dict)+1):

    file_name = img_dict[str(i)]
    cls_ind   = 0 if ONE_CLASS else int( img_lab_dict[str(i)] ) - 1
    data = np.array(Image.open(BEES_PATH + file_name))[:, :, 0] # 1st channel is enough

    # Create boolean mask from array (through jpg-interpolation other values than 0 and 255 are generated)
    data[data <= threshold] = 0 # background
    data[data > threshold]  = 1 # object

    # Compute RLE
    rle = ac.binary_mask_to_rle(data)

    # Calculate area, bbox, height, width
    h, w = rle.get('size')[0], rle.get('size')[1]
    compressed_rle = mask.frPyObjects(rle, h, w)
    area = int(mask.area(compressed_rle))
    bbox = bbox_dict[str(i)]
    # Note: the bbox-format in detectron2 is (xmin, ymin, xmax, ymax)
    bbox[2] = bbox[0] + bbox[2] # xmax
    bbox[3] = bbox[1] + bbox[3] # ymax

    # Create json for COCO
    images.append( {'id': i, 'width': w, 'height': h, 'file_name': file_name} )
    annotations.append( {'segmentation': rle, 'bbox': bbox, 'area': area,
                         'image_id': i, 'category_id': cls_ind, 'iscrowd': 0, 'id': i} )

    if i%10 == 0: print(i)

# Add lists of images and annotations to the validation json
coco_json_train["images"], coco_json_val["images"] = images[:num_train], images[num_train:]
coco_json_train["annotations"], coco_json_val["annotations"] = annotations[:num_train], annotations[num_train:]

json_suffix = '_1' if ONE_CLASS else '_22'
annotations_file = '../metafiles/Bees_Christian/22_species/bees_coco_train' + json_suffix + '.json'
with open(annotations_file, 'w', encoding='utf-8') as f:
    json.dump(coco_json_train, f, ensure_ascii=True, indent=4)
annotations_file = '../metafiles/Bees_Christian/22_species/bees_coco_val' + json_suffix + '.json'
with open(annotations_file, 'w', encoding='utf-8') as f:
    json.dump(coco_json_val, f, ensure_ascii=True, indent=4)