"""
Provides all sorts of plotting methods
"""

import logging
import numpy as np
import preprocessing as pp
from bokeh.plotting import figure, show

logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self):
        pass

    # region Plotting Functions
    @staticmethod
    def plot_sequences(true_train: np.ndarray,
                       true_test: np.ndarray,
                       prediction_sequences: np.ndarray) -> None:
        """
        Plot the training and testing data, along with the sequence of predictions.
        Args:
            true_train (np.ndarray): Training set labels
            true_test (np.ndarray): Testing set labels
            prediction_sequences (np.ndarray): List of predicted sequences

        Returns:

        """
        logger.debug('y_train shape: {}'.format(true_test.shape))
        fig = figure(title='Predictions', plot_width=1300, plot_height=800, active_scroll='wheel_zoom')

        x_train = np.arange(0, len(true_train))
        x_test = np.arange(len(true_train), len(true_train) + len(true_test))
        sequence_length = len(prediction_sequences[0])

        fig.line(x_train, true_train)
        fig.line(x_test, true_test, line_color='orange')

        for i in range(len(prediction_sequences)):
            start_index = len(true_train) + ((i) * sequence_length)
            end_index = start_index + sequence_length
            fig.line(range(start_index, end_index), prediction_sequences[i], line_color='green')

        show(fig)
    # endregion


