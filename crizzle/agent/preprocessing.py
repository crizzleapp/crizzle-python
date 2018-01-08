import logging
import pandas as pd
import numpy as np

# TODO: if output_feature in input_features:
# inputs = windows[:-1] 3d
# outputs = windows[-1] 2d
# TODO: if output_features not in input_features:
# inputs = windows[:] 3d
# outputs = output_features[seqlen:] 2d

logger = logging.getLogger(__name__)


class Preprocessor:
    def __init__(self,
                 dataframe: pd.DataFrame=pd.DataFrame(),
                 sequence_length: int=50,
                 input_features: str='',
                 test_fraction: float=0.1):
        """
        Preprocess data and store metadata for preprocessed data

        Args:
            dataframe (pandas.DataFrame): Full dataset for asset pair with all features
            sequence_length (int): Length of windows in generated x
            input_features (list[str]): Features used as inputs
                We make the assumption that only one feature is used as the output.
            test_fraction (float): Fraction of data to use for validation
        """
        self.dataframe = dataframe[1:]  # remove initial large value
        self.sequence_length = sequence_length
        self.input_features = input_features
        self.test_fraction = test_fraction

        self.inputs = self.dataframe[self.input_features]
        self.inputs_normalized = self.normalize(self.inputs)

    @property
    def raw_y_test(self):
        return self.split(self.inputs, self.test_fraction)[1]

    @staticmethod
    def normalize(dataset: np.ndarray):
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
    def sliding_window(arr: np.ndarray, window_size: int):
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
        return windows[:, None, :]

    @staticmethod
    def chunkify(arr: np.ndarray, chunk_size: int):
        """
        Divide an array into sub-arrays of size N
        NOTE: If chunk size does not exactly divide the array, the array is trimmed at the head.

        Args:
            arr (np.ndarray): Array to divide
            chunk_size (int): Size of each chunk

        Returns:
            np.ndarray: Array of sub-arrays, head-trimmed if necessary
        """
        arr = arr[len(arr) % chunk_size:]
        num_chunks = len(arr)/chunk_size
        logger.debug('Splitting array into {} chunks'.format(num_chunks))
        return np.asarray(np.array_split(arr, num_chunks))[:, None, :]

    @staticmethod
    def split(sequence: np.ndarray, fraction: float):
        train, test = np.split(sequence, [int((1 - fraction) * len(sequence))])
        return train, test

    def process(self,
                sequence_length: int,
                normalize=False) -> tuple:
        """
            Turn a dataframe into a sequence of normalized window-label pairs,
            divided into training and testing sets.

            Args:
                sequence_length (int): Length of input and output sequences

            Returns:
                tuple[np.ndarray]: x_train, x_test, y_train, y_test

            """
        if normalize:
            inputs = self.inputs_normalized
        else:
            inputs = self.inputs
        chunks = self.chunkify(inputs, self.sequence_length)
        logger.debug('Raw data shape: {}'.format(inputs.shape))
        logger.debug('Windows shape: {}'.format(chunks.shape))

        xs = chunks[:-1]
        ys = chunks[1:]
        logger.debug('Xs shape: {}'.format(xs.shape))
        logger.debug('Ys shape: {}'.format(ys.shape))

        x_train, x_test = self.split(xs, self.test_fraction)
        y_train, y_test = self.split(ys, self.test_fraction)
        return x_train, x_test, y_train, y_test


def main():
    arr = np.sin(np.arange(1000))
    pp = Preprocessor()
    print(pp.chunkify(arr, 50).shape)


if __name__=='__main__':
    main()