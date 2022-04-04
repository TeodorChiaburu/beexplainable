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
