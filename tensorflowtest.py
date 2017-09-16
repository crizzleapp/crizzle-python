import os
import logging
import time
import warnings
import argparse
import numpy as np
import data_reader as dr
import preprocessing as pp
import plotting as plt
from predictor import Predictor

# region Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('module')
# endregion

# region Command Line Parameters
parser = argparse.ArgumentParser()
parser.add_argument('-p', help="Currency pair", default='BTC_ETH')
parser.add_argument('-i', help="Sampling interval", default=120)
parser.add_argument('--epochs', help="Number of training epochs", default=1)
parser.add_argument('--seqlen', help="Length of sequences to train LSTM on", default=51)
parser.add_argument('--split', help="Fraction by which to split testing and training data (<1)", default=0.1)
parser.add_argument('--infeatures', nargs='*', help="Input features to use (can use multiple)", default=['open'])
parser.add_argument('--outfeatures', nargs='*', help="Output features to predict", default=['high'])
parser.add_argument('--load', help="Whether to load model from saved file on disk", default=0)
args = parser.parse_args()
logger.debug(args)
# endregion

# region Hyperparameters
model_from_disk = bool(args.load)
currency_pair = args.p
interval = args.i
input_features = args.infeatures
output_features = args.outfeatures
test_fraction = args.split
sequence_length = args.seqlen
epochs = args.epochs

features = list(set(input_features + output_features))
# endregion


if __name__ == '__main__':
    data = dr.load_historical_data(currency_pair, interval, columns=features)
    preprocessor = pp.Preprocessor(data, sequence_length, input_features, output_features, test_fraction)
    windows, x_train, x_test, y_train, y_test = preprocessor.process()

    predictor = Predictor([len(input_features), sequence_length, 100, len(input_features)],
                          from_disk=model_from_disk,
                          filename='model.hdf5')
    predictor.train(x_train, y_train, batch_size=256, epochs=epochs, validation_split=0.1)
    #
    # start = time.time()
    # xs, ax, index = plt.setup_plot(windows, test_fraction)
    # for ix, x in enumerate(x_test):
    #     prediction = (predictor.predict_next_point(x[None, :]))
    #     plt.update_plot(prediction, index + ix)
    # plt.freeze_plot()
    # logger.info('prediction took {} seconds'.format(time.time() - start))
