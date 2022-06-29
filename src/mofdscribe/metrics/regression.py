# -*- coding: utf-8 -*-
"""Metrics for the regression setting."""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from sklearn.metrics import (
    mean_squared_error,
    maen_absolute_error,
    r2_score,
    max_error,
    mean_absolute_percentage_error,
    mean_squared_log_error,
)


def top_n_in_top_k(
    predictions: ArrayLike, labels: ArrayLike, k: int, n: int, maximize: bool = True
) -> int:
    """Find how many of the top n predictions are in the top k labels.

    Args:
        predictions (ArrayLike): predictions for one objective
        labels (ArrayLike): true labels for one objective
        k (int): number of top labels to consider
        n (int): number of top predictions to consider
        maximize (bool): Set to `True` if larger is better.
            Defaults to True.

    Examples:
        >>> predictions = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> labels = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> top_n_in_top_k(predictions, labels, k=2, n=2)
        2

    Returns:
        int: number of top n predictions in top k labels
    """
    indices_predictions = np.argsort(predictions)
    indices_labels = np.argsort(labels)

    if maximize:
        indices_predictions = indices_predictions[::-1]
        indices_labels = indices_labels[::-1]

    top_n_predictions = indices_predictions[:n]
    top_k_labels = indices_labels[:k]

    return np.sum(np.isin(top_n_predictions, top_k_labels))


def get_regression_metrics(predictions: ArrayLike, labels: ArrayLike) -> dict:
    """Get regression metrics.

    Args:
        predictions (ArrayLike): predictions for one objective
        labels (ArrayLike): true labels for one objective

    Returns:
        dict: regression metrics

    Examples:
        >>> predictions = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> labels = [0.1, 0.2, 0.3, 0.4, 0.5]
        >>> get_regression_metrics(predictions, labels)
        {'mae': 0.0,
        'mape': 0.0,
        'mse': 0.0,
        'r2': 1.0,
        'max_error': 0.0,
        'top_5_in_top_5': 5,
        'top_10_in_top_10': 10,
        'top_100_in_top_100': 100,
        'top_500_in_top_500': 500}
    """
    metrics = {
        "mean_squared_error": mean_squared_error(labels, predictions),
        "mae": maen_absolute_error(labels, predictions),
        "r2_score": r2_score(labels, predictions),
        "max_error": max_error(labels, predictions),
        "mean_absolute_percentage_error": mean_absolute_percentage_error(labels, predictions),
        "mean_squared_log_error": mean_squared_log_error(labels, predictions),
        "top_5_in_top_5": top_n_in_top_k(predictions, labels, k=5, n=5),
        "top_10_in_top_10": top_n_in_top_k(predictions, labels, k=10, n=10),
        "top_50_in_top_50": top_n_in_top_k(predictions, labels, k=50, n=50),
        "top_100_in_top_100": top_n_in_top_k(predictions, labels, k=100, n=100),
        "top_500_in_top_500": top_n_in_top_k(predictions, labels, k=500, n=500),
    }

    return metrics
