import os
import time
import logging
import warnings
import numpy as np
import matplotlib.pyplot as plt
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils import plot_model
from keras.models import Sequential, load_model
import read_historical as rh

# region Setup
np.random.seed(0)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
# endregion


# region Pre-Processing
def normalize(dataset):
    return dataset - dataset.mean()


def generate_windows(arr, window_size):
    shape = (arr.shape[0] - window_size + 1, window_size) + arr.shape[1:]
    strides = (arr.strides[0],) + arr.strides
    ret = np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
    return ret


def train_test_split(dataset, test_fraction):
    train, test = np.split(dataset, [int((1 - test_fraction) * len(dataset))])
    x_train = train[:, :-1, :]
    x_test = test[:, :-1, :]
    y_train = train[:, -1]
    y_test = test[:, -1]
    return (x_train, x_test, y_train, y_test)
# endregion


# region Build Model
def build_model(layers):
    """
    :param layers: [data dimensions, sequence length, LSTM layer 2 size, fully connected layer size]
    :return:
    """
    mod = Sequential()
    mod.add(LSTM(layers[1], input_shape=(layers[1], layers[0]),
                 return_sequences=True))
    mod.add(Dropout(0.1))
    mod.add(LSTM(layers[2], return_sequences=False))
    mod.add(Dropout(0.1))
    mod.add(Dense(output_dim=layers[3]))
    mod.add(Activation('tanh'))
    # model.add(Activation('linear'))

    start_time = time.clock()
    mod.compile(loss='mse', optimizer='rmsprop')
    print('Model successfully built.')
    print('Compilation Time: {}'.format(time.clock() - start_time))
    plot_model(mod, show_shapes=True)
    return mod
# endregion


# region Prediction Functions
def predict_next_point(mod, inp):
    predicted = mod.predict(inp)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted


def predict_sequence_full(mod, inp):
    predicted = []
    for i in inp:
        predicted.append(mod.predict(i[None, :, :]))
    return np.array(predicted)


# endregion


# region Plotting Functions
def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()
# endregion


# region Hyperparameters
model_from_disk = False
features = ['close']
test_fraction = 0.1
sequence_length = 11
epochs = 1
prediction_length = 50
# endregion

data = normalize(rh.load_historical_data('BTC_ETH', 30))
windows = rh.generate_windows(data, sequence_length, columns=features)
x_train, x_test, y_train, y_test = train_test_split(windows, 0.1)


if __name__ == '__main__':
    print(windows.shape)
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    if not model_from_disk:
        model = build_model([len(features), sequence_length-1, 100, len(features)])
        start = time.time()
        model.fit(x_train, y_train, batch_size=256, nb_epoch=epochs, validation_split=0.1)
        model.save('model.hdf5')
        print('training took {} seconds'.format(time.time() - start))
    else:
        model = load_model('model.hdf5')
        print('Loaded model from disk')

    start = time.time()
    predictions = predict_sequence_full(model, x_test)
    print('prediction took {} seconds'.format(time.time() - start))
    print(predictions.shape)
    predictions.shape = (predictions.shape[0], predictions.shape[2])
    plot_results(predictions[:, 0], y_test[:, 0])
