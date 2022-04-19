"""Library for constructing CNN classifiers"""

import tensorflow as tf
from tensorflow.keras.layers import Dropout, GlobalAveragePooling2D, Layer
from tensorflow.keras.applications import ResNet50

from typing import Tuple

class CNN_ResNet50(Layer):

    def __init__(self, in_shape: Tuple[int], drop_rate: float,
                 add_global_avg: bool = True, trainable: bool = False, mcdrop: bool = False, weights_file: str = None, **kwargs):
        """Class for a CNN backbone `ResNet50`.

        :param in_shape: Input shape of the images in the format `(width, height, channels)`.
        :type in_shape: tuple of 3 integers.
        :param drop_rate: Dropout rate.
        :type drop_rate: float
        :param add_global_avg: Whether to add a `tf.keras.layers.GlobalsAveragePooling2D` layer after the feature extractor. \
        Some pretrained CNNs come along with such a layer already. Defaults to *True*.
        :type add_global_avg: bool
        :param trainable: Whether the backbone weights should be retrained. Defaults to *False*.
        :type trainable: bool
        :param mcdrop: Whether to apply Monte-Carlo Dropout. Defaults to *False*.
        :type mcdrop: bool
        :param weights_file: Path to load backbone weights from. Defaults to *None*, in which case ImageNet weights are loaded.
        :type weights_file: str, optional
        :param kwargs: Other arguments such as model name.
        """

        super().__init__(**kwargs)

        self.in_shape = in_shape
        self.drop_rate = drop_rate
        self.mcdrop = mcdrop
        if weights_file is None:
            self.resnet = ResNet50(include_top = False, weights = 'imagenet', input_shape = in_shape)
        else:
            self.resnet = tf.keras.models.load_model(weights_file)
        self.global_avg = GlobalAveragePooling2D() if add_global_avg else None
        self.resnet.trainable = trainable

    def call(self, inputs, training: bool = None):
        """Apply forward propagation to **inputs**.

        :param inputs: Tensor batch of shape *(batch_size, height, width, 3)*.
        :type inputs: Tensor
        :param training: Whether to run in training mode (relevant for Batch Normalization). Defaults to *None*.
        :type training: bool, optional
        :return: Features extracted from **inputs**.
        """

        x = self.resnet(inputs, training)
        if self.global_avg is not None:
            x = self.global_avg(x)
        x = Dropout(self.drop_rate, name = 'dropout')(x, training = True if self.mcdrop else training)

        return x

    def get_config(self):
        """Get configuration (needed for serialization when extra arguments are provided in ``__init__()``).

        :return: Configuration dictionary.
        :rtype: dict
        """

        config = super().get_config()
        config.update({"in_shape": self.in_shape, "drop_rate": self.drop_rate,
                       "monte_carlo_dropout": self.mcdrop})

        return config