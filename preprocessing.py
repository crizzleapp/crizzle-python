import logging
import pandas as pd
import numpy as np
from typing import List

# TODO: if output_feature in input_features:
# inputs = windows[:-1] 3d
# outputs = windows[-1] 2d
# TODO: if output_features not in input_features:
# inputs = windows[:] 3d
# outputs = output_features[seqlen:] 2d

logger = logging.getLogger(__name__)


class Preprocessor:
    def __init__(self,
                 dataframe: pd.DataFrame,
                 sequence_length: int,
                 input_features: str,
                 test_fraction: float):
        """
        Preprocess data and store metadata for preprocessed data

        Args:
            dataframe (pandas.DataFrame): Full dataset for asset pair with all features
            sequence_length (int): Length of windows in generated x
            input_features (list[str]): Features used as inputs
                We make the assumption that only one feature is used as the output.
            test_fraction (float): Fraction of data to use for validation
        """
        self.dataframe = dataframe
        self.sequence_length = sequence_length
        self.input_features = input_features
        self.test_fraction = test_fraction

    @staticmethod
    def normalize(dataset):
        """
            Normalize the mean of each feature/column set to 0

            Args:
                dataset (np.ndarray): feature-filtered dataset

            Returns:
                np.ndarray: numpy array of 0-mean features

            """
        means = dataset.mean(axis=0)
        return dataset - means

    @staticmethod
    def generate_windows(arr, window_size):
        """
        Create a list of windows by sliding over the input array

        Args:
            arr (np.ndarray): original numpy array
            window_size (int): length of each window

        Returns:
            np.ndarray: numpy array of windows

        """
        shape = (arr.shape[0] - window_size + 1, window_size) + arr.shape[1:]
        strides = (arr.strides[0],) + arr.strides
        windows = np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
        return windows

    @staticmethod
    def split(sequence, fraction):
        train, test = np.split(sequence, [int((1 - fraction) * len(sequence))])
        return train, test

    def process(self, sequence_length: int) -> tuple:
        """
            Turn a dataframe into a sequence of normalized window-label pairs,
            divided into training and testing sets.

            Args:
                sequence_length (int): Length of input and output sequences

            Returns:
                tuple[np.ndarray]: x_train, x_test, y_train, y_test

            """
        inputs = self.dataframe[self.input_features]  # extract relevant column
        windows = self.generate_windows(inputs, self.sequence_length)
        logger.debug('Windows shape: {}'.format(windows.shape))
        xs = windows[:-1, None, :]
        ys = windows[1:, None, :]
        logger.debug('Xs shape: {}'.format(xs.shape))
        logger.debug('Ys shape: {}'.format(ys.shape))
        x_train, x_test = self.split(xs, self.test_fraction)
        y_train, y_test = self.split(ys, self.test_fraction)
        return x_train, x_test, y_train, y_test
