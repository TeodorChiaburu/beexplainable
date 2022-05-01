"""Library for parsing image inputs before feeding them into the model."""

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from typing import List

def parse_image(file_id: str, img_lookup, img_w: int, img_h: int,
                img_label_lookup = None, cls_lookup = None, root: str = './'):
    """Read image file and resize it to `(img_w, img_h, 3)`.

    :param file_id: ID of the image to read.
    :type file_id: str
    :param img_lookup: Lookup table assigning file ID to file name.
    :type img_lookup: tf.lookup.StaticHashTable
    :param img_w: Image width after resizing.
    :type img_w: int
    :param img_h: Image height after resizing.
    :type img_h: int
    :param img_label_lookup: Lookup table assigning file ID to image label ID. Only needed for the whole dataset. Defaults to None.
    :type img_label_lookup: tf.lookup.StaticHashTable
    :param cls_lookup: Lookup table assigning class ID to class name. Only needed for the whole dataset. Defaults to None.
    :type cls_lookup: tf.lookup.StaticHashTable
    :param root: Root path where the image is stored. Defaults to current folder `./`.
    :type root: str
    :return: Decoded image.
    :rtype: Tensor
    """

    # Retrieve file name from file ID
    filename = img_lookup.lookup(file_id)
    if img_label_lookup is None or cls_lookup is None:
        img = tf.io.read_file(root + filename)
    else:
        lab = img_label_lookup.lookup(file_id) # label of current image
        cls_name = cls_lookup.lookup(lab)
        img = tf.io.read_file(root + cls_name + '/' + filename)
    img = tf.io.decode_jpeg(img, channels = 3)
    img = tf.image.resize(img, [img_w, img_h])

    return img

def parse_to_dataset(file_ids: List[str], labels: List[int], dataset_map, normalize: bool = True):
    """Retrieves file names from **file_ids**, decodes and stores them along with **labels** in a `tf.Dataset`.

    :param file_ids: File IDs to parse images from (will be keys of a dictionary mapping to the file names).
    :type file_ids: list of strings
    :param labels: Class labels corresponding to the images.
    :type labels: list of integers
    :param dataset_map: Function that maps a tuple of filenames and labels to a tuple of parsed images and labels.
    :param normalize: Whether to normalize the image between 0 and 1. Defaults to *True*.
    :type normalize: bool, optional
    :return: Dataset of decoded images and labels.
    :rtype: tf.Dataset
    """

    file_ids = tf.constant(file_ids)
    dataset = tf.data.Dataset.from_tensor_slices((file_ids, labels))
    dataset = dataset.map(dataset_map)

    if normalize:
        normalization_layer = Rescaling(1./255)
        dataset = dataset.map(lambda x, y: (normalization_layer(x), y))

    return dataset