"""Create metafiles for the whole downloaded wildbee dataset (formats inspired by CUB200)"""
"""Only images.txt and images_labels.txt are created here"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob
from beexplainable.utils import metafile_readers as mr

# Metafile folder
bees_folder = "../metafiles/Bees/masked/" #"../metafiles/Bees/raw/"

# Should the 4 similar Bombus species be compressed into one single species?
compress_B_lucorum = True
#bees_subfolder = '22_species/' if compress_B_lucorum else '25_species/'
bees_subfolder = '6_species/'

# Define the 6 species to consider for the jspsych experiment
js_species = ['Andrena_bicolor', 'Andrena_flavipes', 'Andrena_fulva',
              'Bombus_cryptarum', 'Bombus_magnus', 'Bombus_terrestris', 'Bombus_hortorum', 'Bombus_lucorum', 'Bombus_pratorum']

# Read class names
CLASSES_PATH = bees_folder + bees_subfolder + "classes.txt"
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

images = open(bees_folder + "images_6.txt", "a")
image_class_labels = open(bees_folder + bees_subfolder + "image_class_labels.txt", "a")

# Get all paths to the bees, then only keep those relevant for experiment
BEES_PATH = '../../../data/Wildbienen/Bees_masked/' #'../../../data/Wildbienen/Bees/' or '../../../data/data_lstudio/Bees_Christian/'
all_paths = glob.glob(BEES_PATH + '*')
js_paths  = [f for f in all_paths for s in js_species if s in f]

# The full dataset is grouped in species subfolders, Christian's is not
if 'Christian' not in bees_folder:
    img_paths = []
    for jf in js_paths:
        img_paths += glob.glob(jf + '/*.jpg')
else:
    img_paths = js_paths

for i in range(len(img_paths)):

    # Get file name and iscard the common main path
    # Note: for Bees_Christian you are left with file_name.jpg
    #       for Bees you are left with species_folder/file_name.jpg
    file_name = img_paths[i][len(BEES_PATH):]

    # Infer class from file name
    substrs = file_name.split('_')
    # Bees_Christian: ['Andrena', 'bicolor', '73727857', '1.jpg']
    # Bees: ['Andrena', 'bicolor/Andrena', 'bicolor', '73727857', '1.jpg']
    cls = substrs[0] + '_' + substrs[1] if 'Christian' in bees_folder \
            else substrs[0] + '_' + substrs[2]

    # Images are stored in extra species subfolders
    images.write(str(i + 1) + ' ' + file_name + '\n')

    # Compress Bombus lucorum if needed
    if compress_B_lucorum:
        if cls in ['Bombus_cryptarum', 'Bombus_magnus', 'Bombus_terrestris']:
            cls = 'Bombus_lucorum'

    # Get class index from its name and write the pair (file_id, cls_id) to file
    cls_ind = list(cls_dict.keys())[list(cls_dict.values()).index(cls)]
    image_class_labels.write(str(i+1) + ' ' + str(cls_ind) + '\n')

    if i % 1000 == 0: print(i)

images.close()
image_class_labels.close()