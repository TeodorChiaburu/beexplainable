"""Library for parsing image inputs before feeding them into the model."""

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
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

    # Retrieve file name from file ID
    filename = img_lookup.lookup(file_id)
    img = tf.io.read_file(root + filename)
    img = tf.io.decode_jpeg(img, channels = 3)
    img = tf.image.resize(img, [img_w, img_h])

    return img

def parse_image_bbox(file_id: str, img_lookup, bbox_lookup, img_w: int, img_h: int, root: str = './'):
    """Read image file, cropping it to the bounding box and resize it to `(img_w, img_h, 3)`.

    :param file_id: ID of the image to read.
    :type file_id: str
    :param img_lookup: Lookup table assigning file ID to file name.
    :type img_lookup: tf.lookup.StaticHashTable
    :param bbox_lookup: Lookup table assigning filename to BBox coordinates (xmin, ymin, width, height).
    :type bbox_lookup: tf.lookup.DenseHashTable
    :param img_w: Image width after resizing.
    :type img_w: int
    :param img_h: Image height after resizing.
    :type img_h: int
    :param root: Root path where the image is stored. Defaults to current folder `./`.
    :type root: str
    :return: Decoded image.
    :rtype: Tensor
    """

    # Retrieve file name from file ID
    filename = img_lookup.lookup(file_id)
    img = tf.io.read_file(root + filename)
    img = tf.io.decode_jpeg(img, channels=3)
    bbox = bbox_lookup.lookup(file_id) # get coords. from filename
    # Note: the cropping function needs bbox coords as integers in order to manipulate the image on pixel level (also integers)
    img = tf.image.crop_to_bounding_box(img, offset_height = tf.cast(bbox[1], tf.int32), offset_width = tf.cast(bbox[0], tf.int32),
                                             target_height = tf.cast(bbox[3], tf.int32), target_width = tf.cast(bbox[2], tf.int32))
    img = tf.image.resize(img, [img_w, img_h])

    return img

def overlay_mask(img, mask, background_col: List[int] = np.array([255, 255, 255], dtype = np.uint8)):
    """Overlay binary mask over original image. Pixels not belonging to mask are colored differently.

    :param img: Original image.
    :type img: 3D array
    :param mask: Binary matrix.
    :type mask: np.ndarray
    :param background_col: Color to mark background pixels. Defaults to white.
    :type background_col: list of 3 integers for RGB channels
    """

    # Overlay mask on image
    #swap_bin = 255 * (tf.ones_like(mask) - mask)
    #swap_back = tf.stack((swap_bin,) * 3, axis = -1)

    return tf.math.multiply(img, tf.stack((mask,) * 3, axis = -1)) #+ swap_back#img * mask#tf.convert_to_tensor(blank)

def parse_image_mask(file_id: str, img_lookup, masks_tensor, img_w: int, img_h: int, root: str = './'):
    """Read image file, cropping it to the bounding box and resize it to `(img_w, img_h, 3)`.

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

    # Retrieve file name from file ID
    filename = img_lookup.lookup(file_id)
    img = tf.io.read_file(root + filename)
    img = tf.io.decode_jpeg(img, channels=3)

    # Ragged Tensor
    #mask_ind = tf.cast(int(file_id), dtype = tf.int32) - tf.constant(1)
    #mask = tf.gather(masks_tensor.to_tensor(), mask_ind)

    # Dictionary
    # unpack key and value lists
    # ids, masks = list(zip(*masks_tensor.items()))
    # mask_ind = tf.where(ids == file_id)
    # mask_ind = tf.cast(mask_ind, dtype=tf.int32)
    # mask = tf.gather(masks_tensor, mask_ind)

    # DenseHash with Paddings
    #mask = tf.RaggedTensor.from_tensor(masks_tensor.lookup(file_id), padding=-1)

    # DenseHash (masks resized previously)
    mask = masks_tensor.lookup(file_id)

    mask = tf.stack((mask,) * 3, axis = -1)
    img = tf.math.multiply(img, mask) #overlay_mask(img, mask)

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