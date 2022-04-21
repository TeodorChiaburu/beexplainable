"""Create metafiles for the mini wildbee dataset (formats inspired by CUB200)"""

import json

# Path to the annotation file exported from Label Studio
ANNOT_PATH = '../../../data/data_lstudio_export/Bees_Christian/wildbees_part_segmentations.json'

# Open json file
with open(ANNOT_PATH, 'r') as f:
    annot_file = json.load(f)

# Dictionary of part annotations for every image
# Each part is assigned a dictionary containing the mapping from the image index to the list of RLE coords. of the mask
# Note: it is guaranteed that each image contains all body parts masked by one single region
parts = open("../metafiles/parts.txt", "r")
parts_lines = parts.readlines()
parts.close()
parts_dict = {}
for p in parts_lines:
    part_ind, part = p.split(" ")
    part = part.strip("\n")
    parts_dict[part] = part_ind # index as a string

cls_dict = {}
img_count, cls_count = 1, 1 # in CUB format, class and image indices start with 1
# Note! Cross entropy needs to start at 0, make sure to subtract 1 from labels when training

classes = open("../metafiles/classes.txt", "a")
images = open("../metafiles/images.txt", "a")
widths_heights = open("../metafiles/widths_heights.txt", "a")
image_class_labels = open("../metafiles/image_class_labels.txt", "a")
part_locs = open("../metafiles/part_locs.txt", "a") # file index + part index + RLE

# Iterate over images
for annots in annot_file:

    # Get file name (not the whole path) and add it to the dictionary of images
    file_name = annots["data"]["image"]
    file_name = file_name[file_name.rfind('/')+1 : ]
    images.write(str(img_count) + ' ' + file_name + '\n')

    # Infer class from file name
    # If a new class is found, add it to the class dictionary
    substrs = file_name.split('_')
    cls = substrs[0] + '_' + substrs[1]
    if cls not in cls_dict.values():
        cls_dict[cls_count] = cls
        classes.write(str(cls_count) + ' ' + cls + '\n')
        cls_count += 1

    # Add association image to class
    cls_ind = list(cls_dict.keys())[list(cls_dict.values()).index(cls)] # get class index from class name
    image_class_labels.write(str(img_count) + ' ' + str(cls_ind) + '\n')

    # Annotations are stored under 'result'
    annot_result = annots["annotations"][0]["result"]

    # Save img widths and heights
    # For each part, h and w are stored again.
    # It is enough to read h and w from the first part annot (annot_result[0]).
    w, h = annot_result[0]["original_width"], annot_result[0]["original_height"]
    widths_heights.write(str(img_count) + ' ' + str(w) + ' ' + str(h) + '\n')

    # Iterate over part annotations and get RLE coords. for all the regions
    for part_annot in annot_result:
        part = part_annot["value"]["brushlabels"][0] # get the part class
        rle = part_annot["value"]["rle"] # RLE coords
        rle_str = ""
        for rl in rle:
            rle_str += (" " + str(rl))
        part_locs.write(str(img_count) + ' ' + parts_dict[part] + rle_str + '\n')

    img_count += 1

classes.close()
images.close()
widths_heights.close()
image_class_labels.close()
part_locs.close()