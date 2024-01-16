"""Script to create the metafiles for running GradSim as example-based XAI method
The images shown in the Toloka experiment cannot be considered for computing the example-based explanations.
This script copies the images and labels from images.txt and image_class_labels.txt that appear in Toloka
and pastes them in images_tasks123.txt and image_class_labels_tasks123.txt.
The other ones are copied into the *_neighbors.txt files.
"""

import sys
sys.path.insert(1, '../beexplainable')
import glob
from beexplainable.utils import metafile_readers as mr

toloka_imgs = glob.glob('../toloka/fungi/images/task13_imgs/*.JPG')
metafolder = '../metafiles/Fungi/raw/'
IMAGES_PATH = metafolder + 'images.txt'
IMAGES_LABELS_PATH = metafolder + 'image_class_labels.txt'
img_dict = mr.metafile_to_dict(IMAGES_PATH)
img_label_dict = mr.metafile_to_dict(IMAGES_LABELS_PATH)

neighbors_imgs = open('../metafiles/Fungi/raw/toloka_CBR/images_neighbors.txt', 'w')
neighbors_labs = open('../metafiles/Fungi/raw/toloka_CBR/image_class_labels_neighbors.txt', 'w')
tasks123_imgs  = open('../metafiles/Fungi/raw/toloka_CBR/images_tasks123.txt', 'w')
tasks123_labs  = open('../metafiles/Fungi/raw/toloka_CBR/image_class_labels_tasks123.txt', 'w')

for key in img_dict:
    img_id = img_dict[key].split('/')[1].split('.')[0] # i.e. the number in Russula_emetica/2868485470-213821.JPG
    for img in toloka_imgs:
        if img_id in img:
            tasks123_imgs.write(key + ' ' + img_dict[key] + '\n')
            tasks123_labs.write(key + ' ' + img_label_dict[key] + '\n')
            break
    else:
        neighbors_imgs.write(key + ' ' + img_dict[key] + '\n')
        neighbors_labs.write(key + ' ' + img_label_dict[key] + '\n')

neighbors_imgs.close(); neighbors_labs.close()
tasks123_imgs.close(); tasks123_labs.close()