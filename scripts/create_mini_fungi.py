import pandas as pd
import os, shutil

DF_PATH = "../../../data/DanishFungi/"
spec_names = ["Russula emetica", "Russula paludosa", "Russula rosea"]

# Read metafile as csv
metaf = pd.read_csv(DF_PATH + "DF20M-train_metadata_PROD.csv")

# Get image paths that correspond to the relevant species names
# and copy images in separate subfolders
for spec in spec_names:

    # Create species subfolder
    spec_dir = DF_PATH + "DF20M_3spec/" + spec.replace(' ', '_')
    os.makedirs(spec_dir)

    # Filter rows for current species and retrieve img paths
    filtered_df = metaf[metaf['species'] == spec]
    image_paths = filtered_df['image_path'].tolist()

    # Copy images into new species subfolder
    for img in image_paths:
        shutil.copy(DF_PATH + "DF20M/" + img, spec_dir + "/" + img)

    print("Copied " + str(len(image_paths)) + " images for " + spec)