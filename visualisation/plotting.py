"""
Provides all sorts of plotting methods
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
import preprocessing as pp

logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self):
        pass


# region Plotting Functions
def plot_sequences(y_train: np.ndarray,
                   y_test: np.ndarray,
                   prediction_sequences: np.ndarray) -> None:
    """
    Plot the training and testing data, along with the sequence of predictions.
    Args:
        y_train (np.ndarray): Training set labels
        y_test (np.ndarray): Testing set labels
        prediction_sequences (np.ndarray): List of predicted sequences

    Returns:

    """
    pass

# endregion

