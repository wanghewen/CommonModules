# -*- coding:utf-8 -*-
"""Provided data structure related operations such as remove row from matrix."""

__author__ = "Wang Hewen"

ScipyDependencyFlag = False #Check if dependencies are satisfied. If not, some advanced functions will not be defined.
TorchDependencyFlag = False

try:
    import scipy.sparse
    import numpy as np
    ScipyDependencyFlag = True
except Exception:
    ScipyDependencyFlag = False

try:
    import scipy.sparse
    import torch
    import numpy as np
    TorchDependencyFlag = True
except Exception:
    TorchDependencyFlag = False

if ScipyDependencyFlag:
    def PrecisionAtTopK(YTrue, YScore, K=10):
        """
        Used to get Precision at top k

        Refer to https://gist.github.com/mblondel/7337391

        :param Array YTrue: Ground truth array like object with shape = [n_samples]
        :param Array YScore : Predicted scores (should not be labels), array like object with shape = [n_samples]
        :param int K : Top K selected items in YScore
        :return: Result: Precision at top k
        :rtype: float
        Returns
        -------
        precision @k : float
        """
        y_true = YTrue
        y_score = YScore
        k = K

        unique_y = np.unique(y_true)

        if len(unique_y) > 2:
            raise ValueError("Only supported for two relevance levels.")

        pos_label = unique_y[1]
        n_pos = np.sum(y_true == pos_label)

        order = np.argsort(y_score)[::-1]
        y_true = np.take(y_true, order[:k])
        n_relevant = np.sum(y_true == pos_label)

        # Divide by min(n_pos, k) such that the best achievable score is always 1.0.
        return float(n_relevant) / min(n_pos, k)