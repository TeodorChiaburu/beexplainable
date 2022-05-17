"""Library for applying different transformations on original dataset: bbox_cropping, masking etc."""

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from typing import Dict, Tuple
from beexplainable.utils import annot_computers as ac


def crop_images_to_bbox(img_dict: Dict[str, str], bbox_dict: Dict[str, Tuple[float]], src: str, target: str = None):
    """Read images from **img_dict**, crop them to bounding box coords. from **bbox_dict**.

    :param img_dict: Dictionary mapping file IDs to file names.
    :type img_dict: Dict[str, str]
    :param bbox_dict: Dictionary mapping file IDs to bbox coords (returned as floats).
    :type bbox_dict: Dict[str, Tuple[float]]
    :param src: Path to source directory of images.
    :type src: str
    :param target: Path to directory where cropped images should be saved. Defaults to None.
    :type target: str, optional
    """

    for file_id in img_dict:
        filename = img_dict[file_id]
        bbox = bbox_dict[file_id]
        xmin, ymin, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        img = plt.imread(src + filename)
        # Crop image to bbox
        img = img[ymin : ymin+h, xmin : xmin+w]
        if target is not None:
            plt.imsave(target + filename, img)

def mask_body_parts(img_dict: Dict[str, str], contours: np.ndarray, w_h_dict: Dict[str, Tuple[str]], parts_dict: Dict[str, str],
                    src: str, target_overlay: str = None, target_mask: str = None):
    """Read images from **img_dict** and mask body parts with masks from **contours**.

    :param img_dict: Dictionary mapping file IDs to file names.
    :type img_dict: Dict[str, str]
    :param contours: Numpy array containing body part contours for every file ID. \
    Its shape should be *((num_files \dot num_parts) x num_contour_points x 1 x 2)*. The first tuple should contain `(file_id, part_id)`.
    :type contours: np.ndarray
    :param w_h_dict: Dictionary mapping file IDs to tuples of widths and heights for the original image.
    :type w_h_dict: Dict[str, Tuple[str]]
    :param parts_dict: Dictionary mapping file IDs to names of body parts.
    :type parts_dict: Dict[str, str]
    :param src: Path to source directory of images.
    :type src: str
    :param target_overlay: Path to directory where cropped images should be saved. Defaults to None.
    :type target_overlay: str, optional
    :param target_mask: Path to directory where masks should be saved. Defaults to None.
    :type target_mask: str, optional
    """

    # Iterate over contour subarrays (for every file ID there are as many contours as body parts)
    for i in range(0, len(contours), len(parts_dict)):
        # First item in the contour arrays is always a tuple (file_id, part_id)
        file_id = contours[i][0, :, 0][0]
        filename = img_dict[str(file_id)]
        img = plt.imread(src + filename)
        w, h = w_h_dict[str(file_id)] # width and height of current image

        # For every part, read part contours, refill them and mask original image with them
        for j in range(len(parts_dict)):

            part_id = contours[i+j][0, :, 1][0]
            # Get binary mask from contour
            blank = np.zeros((int(h), int(w)), dtype=np.uint8)
            refilled = cv.drawContours(blank, [contours[i + j][1:]], # skip first item which stores file_id and part_id
                                       -1, color=(255, 255, 255),
                                       thickness=-1)//255 # neg. thickness to fill the shape

            if target_mask is not None:
                plt.imsave(target_mask + parts_dict[str(part_id)] + '/' + filename, refilled, cmap = plt.cm.gray)

            # Multiply original image with mask
            overlay = np.copy(img)
            overlay[refilled == 0] = np.array([255, 255, 255], dtype=np.uint8)

            if target_overlay is not None:
                plt.imsave(target_overlay + parts_dict[str(part_id)] + '/' + filename, overlay)


def mask_whole_object(img_dict: Dict[str, str], contours: np.ndarray, w_h_dict: Dict[str, Tuple[str]], parts_dict: Dict[str, str],
                      src: str, target_overlay: str = None, target_mask: str = None, bbox_dict: Dict[str, Tuple[float]] = None):
    """Read images from **img_dict** and mask whole object with union of masks from **contours**. \
    Optionally, crop to bounding box.

    :param img_dict: Dictionary mapping file IDs to file names.
    :type img_dict: Dict[str, str]
    :param contours: Numpy array containing body part contours for every file ID. \
    Its shape should be *((num_files \dot num_parts) x num_contour_points x 1 x 2)*. The first tuple should contain `(file_id, part_id)`.
    :type contours: np.ndarray
    :param w_h_dict: Dictionary mapping file IDs to tuples of widths and heights for the original image.
    :type w_h_dict: Dict[str, Tuple[str]]
    :param parts_dict: Dictionary mapping file IDs to names of body parts.
    :type parts_dict: Dict[str, str]
    :param src: Path to source directory of images.
    :type src: str
    :param target_overlay: Path to directory where cropped images should be saved. Defaults to None.
    :type target_overlay: str, optional
    :param target_mask: Path to directory where masks should be saved. Defaults to None.
    :type target_mask: str, optional
    :param bbox_dict: Dictionary mapping file IDs to bbox coords (returned as floats). Defaults to None.
    :type bbox_dict: Dict[str, Tuple[float]], optional
    """

    # Iterate over contour subarrays (for every file ID there are as many contours as body parts)
    for i in range(0, len(contours), len(parts_dict)):
        # First item in the contour arrays is always a tuple (file_id, part_id)
        file_id = contours[i][0, :, 0][0]
        filename = img_dict[str(file_id)]
        img = plt.imread(src + filename)
        w, h = w_h_dict[str(file_id)] # width and height of current image

        # For every part, read part contours, refill them, build mask for whole object and mask original image with it
        masks = []
        for j in range(len(parts_dict)):
            # Get binary mask from contour
            blank = np.zeros((int(h), int(w)), dtype=np.uint8)
            refilled = cv.drawContours(blank, [contours[i + j][1:]], # skip first item which stores file_id and part_id
                                       -1, color=(255, 255, 255),
                                       thickness=-1)//255 # neg. thickness to fill the shape
            # Note: The empty string is just a placeholder for the part index.
            #       Since we are not interested in that index here, we do not actually read it (empty string instead)
            masks.append(('', refilled))

        # Multiply original image with mask for whole body
        obj_mask = ac.union_of_masks(masks)
        if target_mask is not None:
            plt.imsave(target_mask + filename, obj_mask, cmap = plt.cm.gray)

        overlay = np.copy(img)
        overlay[obj_mask == 0] = np.array([255, 255, 255], dtype=np.uint8)

        # Crop to bounding box, if dictionary provided
        if bbox_dict is not None:
            bbox = bbox_dict[str(file_id)]  # Read bbox coords. from file ID
            xmin, ymin, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            overlay = overlay[ymin : ymin+h, xmin : xmin+w]

        if target_overlay is not None:
            plt.imsave(target_overlay + filename, overlay)