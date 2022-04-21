"""Library for deriving extra annotations from those imported from Label Studio"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../../label_studio_converter') # for scripts
sys.path.insert(2, './beexplainable/label_studio_converter') # for notebooks

import numpy as np
from typing import Tuple, List
from skimage.measure import regionprops
from scipy.ndimage.morphology import binary_closing
from label_studio_converter.brush import decode_rle # comment out before sphinx make html

def rle_to_matrix(rle_arr: np.ndarray, dims: Tuple[int, int]) -> np.ndarray:
    """Converts an array of RLE strings into a 2d matrix of 1s and 0s defining \
    the segmentation mask.

    :param rle_arr: Array of Label Studio RLEs as strings
    :type rle_arr: np.ndarray
    :param dims: Height and width of the segmentation mask (same as original image)
    :type dims: Tuple[int, int]
    :return: 2d matrix (1s for mask, 0s for background)
    :rtype: np.ndarray
    """

    # Note: the decode_rle function in brush.py needs RLEs as ints
    mask = decode_rle(list(map(int, rle_arr))) # 1d array
    # h, w, 4 channels for colors and alpha
    # 1st channel is enough (it is only a gray image)
    mask = np.reshape(mask, (dims[0], dims[1], 4))[:, :, 0]

    # Right now, mask is not binary, since decode_rle smoothens the boundaries out.
    # This results not only pixel values of 0 and 255, but also values in-between.
    # We map all values above threshold to 1 (part of mask) and those below to 0.
    threshold = 50
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            mask[i, j] = 0 if mask[i, j] < threshold else 1

    # Sometimes small pixel regions were not brushed over my the annotators,
    # although they are an inner part of the segment.
    # We correct this through the process of closing (dilation + erosion).
    mask = binary_closing(mask, iterations = 3).astype(np.uint8)

    return mask

def union_of_masks(masks: List[Tuple[str, np.ndarray]]) -> np.ndarray:
    """Computes the union (logical OR) of the matrices in **masks**. \
    The output matrix will be filled with 1s where at least one of the \
    part masks is active and 0s otherwise.

    :param masks: List of tuples (part_name, 2d mask array).
    :type masks: List[Tuple[str, np.ndarray]]
    :return: 2d mask array for the whole object
    :rtype: np.ndarray
    """

    # Initialize object mask with first part mask
    obj_mask = masks[0][1]
    for i in range(1, len(masks)):
        # Compute logical OR for all the following masks
        obj_mask = np.logical_or(obj_mask, masks[i][1]).astype(np.uint8)

    return obj_mask

def cub_bbox_from_mask(obj_mask: np.ndarray) -> Tuple[float]:
    """Computes the bounding box coordinates from an object segmentation mask \
    in the CUB format: *xmin, ymin, width, height*.

    :param obj_mask: Binary segmentation matrix for the whole object.
    :type obj_mask: np.ndarray
    :return: Tuple of 4 BBox coordinates.
    :rtype: Tuple[float]
    """

    # Note: regionprops[0].bbox = [ymin, xmin, ymax, xmax]
    bbox = regionprops(obj_mask)[0].bbox

    # Get BBox coords. according to CUB format (xmin, ymin, w, h)
    return float(bbox[1]), float(bbox[0]), float(bbox[3] - bbox[1]), float(bbox[2] - bbox[0])

def binary_mask_to_indexes(bin_mask: np.ndarray, output_as_strings: bool = True) -> List:
    """Returns the 1D-indexes of the 1's in a binary 2d array.

    :param bin_mask: Binary 2d array.
    :type bin_mask: np.ndarray
    :param output_as_strings: Whether to return the indexes as strings (for storing into file). If *False*, \
    indexes are returned as integers. Defaults to *True*.
    :type output_as_strings: bool
    :return: List of iD indexes of 1's.
    :rtype: list of strings or integers
    """

    cols = bin_mask.shape[1]
    # Get 2d indexes of 1's
    mask_ind_2d = np.argwhere(bin_mask == 1)

    if output_as_strings:
        mask_ind_1d = [str(ind[0]*cols + ind[1]) for ind in mask_ind_2d]
    else:
        mask_ind_1d = [ind[0]*cols + ind[1] for ind in mask_ind_2d]

    return mask_ind_1d