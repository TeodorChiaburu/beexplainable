# XAI Experiments on a dataset of wild bees

## Data Acquisition

The script [webscraper_inat.py](beexplainable/webscraper_inat.py) downloads photos of bees from [iNaturalist](https://www.inaturalist.org/observations). The user only needs to specify in the *main* section the target folder where the photos should be downloaded, a maximum number of photos to search for and the corresponding url index of the species. 

For instance, to find the index for the species *Anthidium manicatum*, type the species name in the search bar of the *iNaturalist* site and copy the number at the end of the url (it should be 62453).
