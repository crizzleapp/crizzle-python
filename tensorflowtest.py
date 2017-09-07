import datetime
import logging
import random

import read_historical as rh
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
np.random.seed(0)


# TODO: replace feed_dicts with queues

# SET LOGGING LEVELS
logging_level = logging.INFO
logging.basicConfig(level=logging_level)

length = 10
test = np.array(range(100))


def normalize(array):
    normed = (array - np.mean(array, axis=0)) / np.std(array, axis=0)
    return normed

test = normalize(test)
lol = np.array([test[start:start + length] for start in range(0, len(test) - length + 1)])
training_set = lol[:900]
validation_set = lol[900:]


if __name__ == '__main__':
    print(test)
