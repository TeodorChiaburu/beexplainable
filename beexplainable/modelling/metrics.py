"""Library for custom metrics"""

import numpy as np

def inception_score(p_yx, eps=1e-16):
    """Calculate the inception score for p(y|x).
    See https://machinelearningmastery.com/how-to-implement-the-inception-score-from-scratch-for-evaluating-generated-images/

    :param p_yx: Predictions (as probabilities) for samples *x*.
    :type p_yx: np.array of shape `num_samples x num_classes`
    :param eps: Extra term to avoid log(0). Defaults to 1e-16.
    :type eps: float
    :return: Inception Score for the given predictions.
    """

    # Calculate p(y) - marginal probability
    p_y = np.expand_dims(p_yx.mean(axis=0), 0)
    # KL divergence for each image
    kl_d = p_yx * (np.log(p_yx + eps) - np.log(p_y + eps))
    # sum over classes
    sum_kl_d = kl_d.sum(axis=1)
    # average over images
    avg_kl_d = np.mean(sum_kl_d)
    # undo the logs
    is_score = np.exp(avg_kl_d)

    return is_score