import logging
import os
import time
import warnings

import numpy as np
import pandas as pd

from preprocessing import Preprocessor
from data_reader import DataReader
from predictor import Predictor
from plotting import Plotter

# TODO: ADD LOGGING TO ALL MODULES

# region Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('module')
# endregion

# region Hyperparameters
data_dir = 'data\\historical'
model_from_disk = False
currency_pair = 'BTC_ETH'
interval = 120
input_feature = 'open'
test_fraction = 0.1
sequence_length = 200
epochs = 200

# endregion


if __name__ == '__main__':
    # TODO: move this into main()
    # TODO: have main() return status codes
    dr = DataReader([currency_pair], interval, data_dir)
    # data = dr.dataframes[currency_pair]
    data = pd.DataFrame(np.sin(np.arange(0, 100, 0.01)), columns=[input_feature])
    pp = Preprocessor(data, sequence_length, input_feature, test_fraction)
    plt = Plotter()

    x_train, x_test, y_train, y_test = pp.process(sequence_length, normalize=True)

    predictor = Predictor(sequence_length,
                          from_disk=model_from_disk,
                          filename='model.hdf5')
    if not model_from_disk:
        predictor.train(x_train, y_train, (x_test, y_test), batch_size=256, epochs=epochs)
    start = time.time()
    predictions = predictor.predict_next(x_test)
    print('Prediction time: {}'.format(time.time() - start))
    plt.plot_sequences(pp.raw_y_test, predictions)

    # xs, ax, index = plt.setup_plot(windows, test_fraction)
    # for ix, x in enumerate(x_test):
    #     prediction = (predictor.predict_next_point(x[None, :]))
    #     plt.update_plot(prediction, index + ix)
    # plt.freeze_plot()
    # logger.info('prediction took {} seconds'.format(time.time() - start))
