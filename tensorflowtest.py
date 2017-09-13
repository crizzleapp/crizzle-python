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


def train_test_split(dataset, fraction):
    train, test = np.split(dataset, [int((1 - fraction) * len(dataset))])
    x_train = train[None, :, :-1, :]
    x_test = test[None, :, :-1, :]
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
    predicted = mod.predict(inp).squeeze()
    return predicted


def predict_sequence_full(mod, inp):
    predicted = []
    for i in inp:
        predicted.append(mod.predict(i[None, :, :]))
    return np.array(predicted)


# endregion


# region Plotting Functions
def plot_results(predicted_data, full_dataset, fraction):
    true_data = train_test_split(full_dataset, fraction)
    xs = range(len(full_dataset))
    fig = plt.figure(facecolor='white', figsize=(8, 5))
    ax = fig.add_subplot(111)
    ax.plot(xs[:len(true_data[2])], true_data[2][:, 0], label='Train Data')
    ax.plot(xs[len(true_data[2]):], true_data[3][:, 0], label='Test Data')
    plt.plot(xs[len(true_data[2]):], predicted_data, label='Predicted')
    plt.legend()
    plt.show()


def setup_plot(full_dataset, fraction):
    plt.ion()
    true_data = train_test_split(full_dataset, fraction)
    xs = range(len(full_dataset))
    fig = plt.figure(facecolor='white', figsize=(8, 5))
    ax = fig.add_subplot(111)
    ax.plot(xs[:len(true_data[2])], true_data[2][:, 0], label='Train Data')
    ax.plot(xs[len(true_data[2]):], true_data[3][:, 0], label='Test Data')
    plt.legend()
    plt.pause(0.01)
    return (xs, ax, len(true_data[2]))


def freeze_plot():
    plt.ioff()
    plt.show()


def update_plot(predicted_data, xs, split_index):
    plt.plot(xs[split_index:], predicted_data[0][:][0])
    plt.pause(0.01)
# endregion


# region Hyperparameters
model_from_disk = True
interval = 30
features = ['close']
test_fraction = 0.1
sequence_length = 11
epochs = 1
# endregion

data = normalize(rh.load_historical_data('BTC_ETH', interval))
windows = rh.generate_windows(data, sequence_length, columns=features)
x_train, x_test, y_train, y_test = train_test_split(windows, test_fraction)
print(x_train.shape)
print(y_train.shape)


if __name__ == '__main__':
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
    predictions = []
    xs, ax, index = setup_plot(windows, test_fraction)
    for x in x_test:
        predictions.append(model.predict(x[:, :-1]))
        update_plot(predictions, xs, index)
    print('prediction took {} seconds'.format(time.time() - start))
