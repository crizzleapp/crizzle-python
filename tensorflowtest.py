import os
import logging
import time
import warnings
import numpy as np

import data_reader as dr
import preprocessing as pp
import plotting as plt
import predictor

# TODO: API-ify this file

# region Setup
np.random.seed(0)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
# endregion

# region Hyperparameters
model_from_disk = False
interval = 30
input_features = ['high']
output_features = ['high']
test_fraction = 0.1
sequence_length = 201
epochs = 10
feature_indices = [input_features.index(o) for o in output_features]
# endregion

data = pp.normalize(dr.select(dr.load_historical_data('BTC_ETH', interval), column_list=input_features))
windows = pp.generate_windows(data, sequence_length)
x_train, x_test, y_train, y_test = pp.train_test_split(windows, test_fraction)


if __name__ == '__main__':
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
