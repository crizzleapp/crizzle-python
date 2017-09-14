import os
import logging
import time
import warnings
import argparse
import numpy as np
import data_reader as dr
import preprocessing as pp
import plotting as plt
import predictor

# region Setup
np.random.seed(0)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
# endregion

# region Command Line Parameters
parser = argparse.ArgumentParser()
parser.add_argument('-p', help="Currency pair", default='BTC_ETH')
parser.add_argument('-i', help="Sampling interval", default=30)
parser.add_argument('--epochs', help="Number of training epochs", default=1)
parser.add_argument('--seqlen', help="Length of sequences to train LSTM on", default=51)
parser.add_argument('--split', help="Fraction by which to split testing and training data (<1)", default=0.1)
parser.add_argument('--infeatures', nargs='*', help="Input features to use (can use multiple)", default=['close'])
parser.add_argument('--outfeatures', nargs='*', help="Output features to predict", default=['close'])
parser.add_argument('--load', help="Whether to load model from saved file on disk", default=0)
args = parser.parse_args()
print(args)
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
feature_indices = [input_features.index(o) for o in output_features]
# endregion


if __name__ == '__main__':
    data = dr.load_historical_data(currency_pair, interval, columns=input_features)
    x_train, x_test, y_train, y_test = pp.preprocess(data, sequence_length, test_fraction)

    if not model_from_disk:
        model = predictor.build_model([len(input_features), sequence_length - 1, 100, len(input_features)])
        start = time.time()
        model.fit(x_train, y_train, batch_size=256, nb_epoch=epochs, validation_split=0.1)
        model.save('model.hdf5')
        print('training took {} seconds'.format(time.time() - start))
    else:
        model = predictor.load_model('model.hdf5')
        print('Loaded model from disk')

    start = time.time()
    xs, ax, index = plt.setup_plot(windows, test_fraction)
    for ix, x in enumerate(x_test):
        prediction = (predictor.predict_next_point(model, x[None, :], feature_indices))
        plt.update_plot(prediction, index+ix)
    plt.freeze_plot()
    print('prediction took {} seconds'.format(time.time() - start))
