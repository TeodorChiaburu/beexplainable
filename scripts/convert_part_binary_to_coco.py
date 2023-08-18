"""Script to convert body part masks into the COCO format"""

import json
from pycocotools import mask
import numpy as np
from PIL import Image
from beexplainable.utils import metafile_readers as mr
from beexplainable.utils import annot_computers as ac

# Metafile paths
BEES_PATH = '../../../data/data_lstudio/Bees_Christian_masks_bbox/'
PARTS_PATH = '../metafiles/Bees_Christian/parts.txt'
IMAGES_PATH = '../metafiles/Bees_Christian/images.txt'
IMAGES_LABELS_PATH = '../metafiles/Bees_Christian/22_species/image_class_labels.txt'

# Read metafiles into dictionary
parts_dict = mr.metafile_to_dict(PARTS_PATH)
num_parts = len(parts_dict)
img_dict = mr.metafile_to_dict(IMAGES_PATH)
img_lab_dict = mr.metafile_to_dict(IMAGES_LABELS_PATH)

# Define json file for COCO data; it will include lists for categories/classes, images and annotations
coco_json_train, coco_json_val = {}, {}
images, annotations = [], []
# Note: the json files will be used in the detectron2 library, which requires classes to start at index 0!
categories = [{"id": int(p)-1, "name": parts_dict[p]} for p in parts_dict]
coco_json_train["categories"] = coco_json_val["categories"] = categories

# Iterate through images and create json entries
threshold = 50  # see ac.rle_to_matrix()
num_train = 500 # how many images should go into the json used for training
for i in range(1, len(img_dict)+1):
    file_name = img_dict[str(i)]

    for p in parts_dict:

        cls_ind, cls_name = int(p)-1, parts_dict[p] # the body parts give the class index and name
        data = np.array(Image.open(BEES_PATH + cls_name + '/' + file_name))[:, :, 0] # 1st channel is enough

        # Create boolean mask from array (through jpg-interpolation other values than 0 and 255 are generated)
        data[data <= threshold] = 0 # background
        data[data > threshold]  = 1 # object

        # Compute RLE
        rle = ac.binary_mask_to_rle(data)

        # Calculate area, bbox, height, width
        h, w = rle.get('size')[0], rle.get('size')[1]
        compressed_rle = mask.frPyObjects(rle, h, w)
        area = int(mask.area(compressed_rle))

        # Compute bbox in CUB format first
        bbox = list( ac.cub_bbox_from_mask(data) )
        # Note: the bbox-format in detectron2 is (xmin, ymin, xmax, ymax)
        bbox[2] = bbox[0] + bbox[2] # xmax
        bbox[3] = bbox[1] + bbox[3] # ymax

        # Create json item for part mask
        annotations.append( {'segmentation': rle, 'bbox': bbox, 'area': area,
                             'image_id': i, 'category_id': cls_ind, 'iscrowd': 0, 'id': num_parts*(i-1)+int(p)} )

    # Create json item for whole image
    images.append({'id': i, 'width': w, 'height': h, 'file_name': file_name})
    if i%10 == 0: print(i)

# Add lists of images and annotations to the validation json
coco_json_train["images"], coco_json_val["images"] = images[:num_train], images[num_train:]
coco_json_train["annotations"], coco_json_val["annotations"] = annotations[:num_train*num_parts], annotations[num_train*num_parts:]

annotations_file = '../metafiles/Bees_Christian/22_species/bees_coco_train_3_cropped.json'
with open(annotations_file, 'w', encoding='utf-8') as f:
    json.dump(coco_json_train, f, ensure_ascii=True, indent=4)
annotations_file = '../metafiles/Bees_Christian/22_species/bees_coco_val_3_cropped.json'
with open(annotations_file, 'w', encoding='utf-8') as f:
    json.dump(coco_json_val, f, ensure_ascii=True, indent=4)