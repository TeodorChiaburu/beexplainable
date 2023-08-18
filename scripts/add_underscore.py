"""Rename a subfolder name from 'Genus species' to 'Genus_species'"""

import os

PARENT_PATH = '../../../data/KInsecta_webapp_data_2022_09_02/ilona_squared/train/'
os.chdir(PARENT_PATH)

for subfold in os.listdir('.'):
    genus, species = subfold.split(' ')
    os.rename(subfold, genus + '_' + species)