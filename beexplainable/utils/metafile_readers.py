"""Library for opening metafiles and converting them into dictionaries"""

from typing import Dict, List

def metafile_to_dict(metafile_path: str) -> Dict[str, str]:
    """Opens file from **metafile_path** and returns it as a dictionary os strings. \
    Note that this function works as intended only for files containing simple \
    key to value mappings, such as *classes.txt*. For more complex mappings, \
    such as in *part_locs.txt*, special functions were defined below.

    :param metafile_path: Path to the file to be read.
    :type metafile_path: str
    :return: Dictionary of type 'id-to-id' or 'id-to-name'.
    :rtype: Dict[str, str]
    """

    # Read the metafile
    metafile = open(metafile_path, "r")

    # Read the file line by line, split each line into key and value (separated
    # by white space) and store them in a dictionary
    return {ml.split()[0]: ml.split()[1] for ml in metafile.readlines()}


def part_locs_to_dict(metafile_path: str) -> Dict[str, Dict[str, List[str]]]:
    """Opens file containing part locations and returns it as a dictionary. \
    The key is the *file id* and it is mapped to a second dictionary containing \
    the mappings from the *part id* to the RLEs.

    :param metafile_path: Path to the file to be read.
    :type metafile_path: str
    :return: Dictionary of type 'file_id to RLEs (for each part)'.
    :rtype: Dict[str, Dict[str, List[str]]]
    """

    # Read the metafile
    metafile = open(metafile_path, "r")
    metalines = metafile.readlines() # list of strings separated by white spaces

    metadict = {}
    # Files are sorted increasingly according to file_id
    # Therefore, all body parts for each image are stored together in 3-line-chunks
    for i in range(0, len(metalines), 3):
        parts_dict = {}
        for j in range(3):
            ml = metalines[i+j].split() # current line is split into strings
            parts_dict[ml[1]] = ml[2:] # 2nd str is the body part id, all the following are its RLE coords.

        file_id = ml[0] # only needed once, because similar for every part of current img
        metadict[file_id] = parts_dict

    return metadict