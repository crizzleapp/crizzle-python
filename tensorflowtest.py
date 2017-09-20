import logging
import os
import time
import warnings

import preprocessing as pp
from data_reader import DataReader
from predictor import Predictor

# TODO: ADD LOGGING TO ALL MODULES

# region Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('module')
# endregion

# region Hyperparameters
data_dir = 'data\\historical'
model_from_disk = True
currency_pair = 'BTC_ETH'
interval = 5
input_feature = 'open'
test_fraction = 0.1
sequence_length = 50
epochs = 5

# endregion


if __name__ == '__main__':
    # TODO: move this into main()
    # TODO: have main() return status codes
    dr = DataReader([currency_pair], interval, data_dir)
    data = dr.dataframes[currency_pair]
    preprocessor = pp.Preprocessor(data, sequence_length, input_feature, test_fraction)
    x_train, x_test, y_train, y_test = preprocessor.process(sequence_length)

    predictor = Predictor(sequence_length,
                          from_disk=model_from_disk,
                          filename='model.hdf5')
    if not model_from_disk:
        predictor.train(x_train, y_train, batch_size=256, epochs=epochs, validation_split=0.1)
    start = time.time()
    print(predictor.predict_next(x_test))
    print('Prediction time: {}'.format(time.time() - start))

    # xs, ax, index = plt.setup_plot(windows, test_fraction)
    # for ix, x in enumerate(x_test):
    #     prediction = (predictor.predict_next_point(x[None, :]))
    #     plt.update_plot(prediction, index + ix)
    # plt.freeze_plot()
    # logger.info('prediction took {} seconds'.format(time.time() - start))
