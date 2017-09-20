import os
import logging
import time
import warnings
import argparse
import numpy as np
from data_reader import DataReader
import preprocessing as pp
import plotting as plt
from predictor import Predictor

# TODO: ADD LOGGING TO ALL MODULES

# region Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('module')
# endregion

# region Hyperparameters
model_from_disk = False
currency_pair = 'BTC_ETH'
interval = 120
input_feature = 'open'
test_fraction = 0.1
sequence_length = 50
epochs = 1

# endregion


if __name__ == '__main__':
    # TODO: move this into main()
    # TODO: have main() return status codes
    dr = DataReader(['BTC_ETH'], 30)
    data = dr.dataframes['BTC_ETH']
    preprocessor = pp.Preprocessor(data, sequence_length, input_feature, test_fraction)
    x_train, x_test, y_train, y_test = preprocessor.process(sequence_length)

    predictor = Predictor(sequence_length - 1,
                          from_disk=model_from_disk,
                          filename='model.hdf5')
    predictor.train(x_train, y_train, batch_size=256, epochs=epochs, validation_split=0.1)

    # start = time.time()
    # xs, ax, index = plt.setup_plot(windows, test_fraction)
    # for ix, x in enumerate(x_test):
    #     prediction = (predictor.predict_next_point(x[None, :]))
    #     plt.update_plot(prediction, index + ix)
    # plt.freeze_plot()
    # logger.info('prediction took {} seconds'.format(time.time() - start))
