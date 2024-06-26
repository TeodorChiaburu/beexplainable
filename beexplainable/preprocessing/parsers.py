"""Library for parsing image inputs before feeding them into the model."""

import tensorflow as tf
from typing import List

def parse_image(file_id: str, img_lookup, img_w: int, img_h: int, root: str = './'):
    """Read image file and resize it to `(img_w, img_h, 3)`.

    :param file_id: ID of the image to read.
    :type file_id: str
    :param img_lookup: Lookup table assigning file ID to file name.
    :type img_lookup: tf.lookup.StaticHashTable
    :param img_w: Image width after resizing.
    :type img_w: int
    :param img_h: Image height after resizing.
    :type img_h: int
    :param root: Root path where the image is stored. Defaults to current folder `./`.
    :type root: str
    :return: Decoded image.
    :rtype: Tensor
    """

    # Retrieve file name from file ID, read image and resize
    filename = img_lookup.lookup(file_id)
    img = tf.io.read_file(root + filename)
    img = tf.io.decode_jpeg(img, channels = 3)
    img = tf.image.resize(img, [img_w, img_h])

    return img

def parse_image_and_mask(file_id: str, img_lookup, img_w: int, img_h: int, root_img: str = './', root_mask: str = './masks/'):
    """Read image file, resize it to `(img_w, img_h, 3)` and read object mask and resize it to `(img_w, img_h, 1)`.

    :param file_id: ID of the image to read.
    :type file_id: str
    :param img_lookup: Lookup table assigning file ID to file name.
    :type img_lookup: tf.lookup.StaticHashTable
    :param img_w: Image width after resizing.
    :type img_w: int
    :param img_h: Image height after resizing.
    :type img_h: int
    :param root_img: Root path where the image is stored. Defaults to current folder `./`.
    :type root_img: str
    :param root_mask: Root path where the mask is stored. Defaults to current folder `./masks/`.
    :type root_mask: str
    :return: Decoded image and binary mask
    :rtype: Tuple[Tensor, Tensor]
    """
    # Retrieve file name from file ID, read image and resize
    filename = img_lookup.lookup(file_id)
    img = tf.io.read_file(root_img + filename)
    img = tf.io.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [img_w, img_h])

    # Read binary mask and resize it accordingly
    mask = tf.io.read_file(root_mask + filename)
    mask = tf.io.decode_jpeg(mask, channels=1)
    mask = tf.image.resize(mask, [img_w, img_h], method = 'nearest') # use nearest interpolation to preserve edge sharpness
    mask = tf.where(mask > 200, 1.0, 0.0) # remove resizing artifacts and normalize to 0.0-1.0

    return img, mask

def parse_to_dataset(file_ids: List[str], labels: List[int], dataset_map):
    """Retrieves file names from **file_ids**, decodes and stores them along with **labels** in a `tf.Dataset`.

    :param file_ids: File IDs to parse images from (will be keys of a dictionary mapping to the file names).
    :type file_ids: list of strings
    :param labels: Class labels corresponding to the images.
    :type labels: list of integers
    :param dataset_map: Function that maps a tuple of filenames and labels to a tuple of parsed images and labels.
    :return: Dataset of decoded images and labels.
    :rtype: tf.Dataset
    """

    file_ids = tf.constant(file_ids)
    dataset = tf.data.Dataset.from_tensor_slices((file_ids, labels))
    dataset = dataset.map(dataset_map)

    return dataset