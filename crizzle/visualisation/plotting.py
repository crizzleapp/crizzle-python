"""
Provides all sorts of plotting methods
"""

import logging

import numpy as np
from bokeh.plotting import figure, show

logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self):
        pass

    # region Plotting Functions
    @staticmethod
    def plot_sequences(test_ys: np.ndarray,
                       predictions: np.ndarray) -> None:
        """
        Plot the training and testing data, along with the sequence of predictions.

        Args:
            test_ys (np.ndarray): Training set labels
            true_test (np.ndarray): Testing set labels
            predictions (np.ndarray): List of predicted sequences
        """
        logger.debug('true data shape: {}'.format(test_ys.shape))
        logger.debug('prediction shape: {}'.format(predictions.shape))
        fig = figure(title='Predictions', plot_width=1300, plot_height=800, active_scroll='wheel_zoom')

        x = np.arange(len(test_ys))
        sequence_length = len(predictions[0])

        fig.line(x, test_ys, line_color='orange')

        print(predictions.shape)
        for i in range(len(predictions)):
            # start_index = len(true_data) + ((i) * sequence_length)
            start_index = 0
            end_index = start_index + ((i + 1) * sequence_length)
            fig.line(range(start_index, end_index), predictions[i], line_color='green')

        show(fig)
    # endregion


