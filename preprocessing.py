import numpy as np

# region Pre-Processing
def normalize(dataset):
    dataset = np.array(dataset)
    mean = dataset.mean(axis=0)
    return dataset - mean


def generate_windows(arr, window_size):
    arr = np.array(arr)
    shape = (arr.shape[0] - window_size + 1, window_size) + arr.shape[1:]
    strides = (arr.strides[0],) + arr.strides
    ret = np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
    return ret


def train_test_split(dataset, fraction):
    train, test = np.split(dataset, [int((1 - fraction) * len(dataset))])
    x_train = train[:, :-1, :]
    x_test = test[:, :-1, :]
    y_train = train[:, -1]
    y_test = test[:, -1]
    return x_train, x_test, y_train, y_test
# endregion
