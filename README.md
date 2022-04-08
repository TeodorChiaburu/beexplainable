# XAI Experiments on a dataset of wild bees

## Data Acquisition

The script [webscraper_inat.py](scripts/webscraper_inat.py) downloads 
photos of bees from [iNaturalist](https://www.inaturalist.org/observations). 
The user only needs to specify in the *main* section the target folder where 
the photos should be downloaded, a maximum number of photos to search for 
and the corresponding url index of the species. 

For instance, to find the index for the species *Anthidium manicatum*, 
type the species name in the search bar of the *iNaturalist* site and 
copy the number at the end of the url (it should be 62453).

**To Do**: can't load more than 100 pages. After the 100th page, the 
browser is requesting log-in credentials. 


## Data Preprocessing

The script [create_metafiles.py](scripts/create_metafiles.py) creates 
metafiles from the json-files downloaded from Label Studio similar to the 
**CUB200** format. The files created are:

- *classes.txt* - each class name is allocated a unique identifier from 1 to 25
- *images.txt* - each jpg-file is given a unique identifier from 1 to 726
- *image_class_labels.txt* - each file ID is mapped to the corresponding class ID
- *parts.txt* - each relevant body part is given an ID from 1 to 3
- *part_locs.txt* - each body part from each file is mapped to its RLE coordinates; 
each row starts with the file ID followed by the body part ID followed by the list of 
RLE coordinates

### Important Note on the `RLE` Format

Beware that the `RLE` format used by Label Studio to store segmentation masks is not 
the same commonly known `RLE` format from the **COCO** dataset. The `RLE` numbers in 
the **COCO** standard are interpreted as pixel counts, while the Label Studio coordinates 
stand for ... Please follow this [issue](https://github.com/heartexlabs/label-studio-converter/issues/95) 
for further details.

### Decoding `RLE` into Segmentation Masks

For translating the `RLE` coordinates into segmentation matrices, the library 
[label-studio-converter](https://github.com/heartexlabs/label-studio-converter) 
was used. Every image is accompanied by three part annotations:

- *Head* - includes the whole head of the insect along with its tentacles
- *Thorax* - middle body together with legs and wings
- *Abdomen* - lower body including needle, if present

The picture below shows the segmentation masks - binary and overlaid - 
in the case of an *Osmia bicornis*. More examples can be found in 
[figures](figures). The *xml* file to recreate the 
annotation task in Label Studio can be downloaded from ... (*Link zum 
eigenen LS repo*).

![Example of mask visualization](figures/Masks_Osmia_bicornis_25948103_1.png)
