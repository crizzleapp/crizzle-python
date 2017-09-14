from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils import plot_model
from keras.models import Sequential, load_model
import numpy as np
import logging
import time

logger = logging.getLogger(__name__)


# region Build Model
def build_model(layers):
    """
    Build model given layer sizes
    :param layers: [data dimensions, sequence length, LSTM layer 2 size, fully connected layer size]
    :return: keras model
    """
    mod = Sequential()
    mod.add(LSTM(layers[1], input_shape=(layers[1], layers[0]),
                 return_sequences=True))
    mod.add(Dropout(0.1))
    mod.add(LSTM(layers[2], return_sequences=False))
    mod.add(Dropout(0.1))
    mod.add(Dense(units=layers[3]))
    mod.add(Activation('tanh'))
    start_time = time.clock()
    mod.compile(loss='mse', optimizer='rmsprop')
    print('Model successfully built.')
    print('Compilation Time: {}'.format(time.clock() - start_time))
    try:
        plot_model(mod, show_shapes=True)
        logger.debug('Saved graph to image.')
    except:
        logger.error('''Error saving graph to image. 
        Make sure you have correctly installed the Graphviz executables and PyDot.''')
    return mod
# endregion


#region Training
def train(model, inputs, labels, batch_size=256, epochs=1, validation_split=0.1):
    start = time.clock()
    model.fit(inputs, labels, batch_size=batch_size, epochs=epochs, validation_split=validation_split)
    model.save('model.hdf5')
    print('training took {} seconds'.format(time.time() - start))



# region Prediction Functions
def predict_next_point(mod, inp, feature_indices):
    predicted = mod.predict(inp).squeeze()
    if predicted.shape != ():
        predicted = [predicted[i] for i in feature_indices]
    return predicted


def predict_sequence_full(mod, inp, feature_indices):
    predicted = []
    for i in inp:
        predicted.append(predict_next_point(mod, i, feature_indices))
    return np.array(predicted).squeeze()
# endregion
