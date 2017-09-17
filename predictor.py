from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils import plot_model
from keras.models import Sequential, load_model
import numpy as np
import logging
import time


# TODO: implement many-to-many prediction

class Predictor:
    """
    Keras-based price predictor
    """
    def __init__(self, layers, from_disk=False, filename=None):
        self.logger = logging.getLogger(__name__)
        self.layers = layers

        if from_disk:
            try:
                self.load_model_from_disk(filename)
            except OSError as e:
                self.logger.error('INVALID FILENAME')
                raise e
        else:
            self.model = self.build(self.layers)

    def load_model_from_disk(self, filename):
        self.model = load_model(filename)
        self.logger.info('Loaded model from disk.')

    def build(self, layers):
        """
            Build model given layer sizes
            :param layers: [data dimensions, sequence length, LSTM layer 2 size, fully connected layer size]
            :return: keras model
            """
        mod = Sequential()
        mod.add(LSTM(layers[1], input_shape=(layers[1], layers[0]),
                     return_sequences=True))
        mod.add(Dense(units=layers[3]))

        start_time = time.clock()
        mod.compile(loss='mse', optimizer='rmsprop')
        print('Model built successfully.')
        print('Build time: {}'.format(time.clock() - start_time))
        try:
            plot_model(mod, show_shapes=True)
            self.logger.debug('Saved graph to image.')
        except:
            self.logger.error('''Error saving graph to image. 
                Make sure you have correctly installed the Graphviz executables and PyDot.''')
        return mod

    def train(self, inputs, labels, batch_size=256, epochs=1, validation_split=0.1):
        start = time.clock()
        self.model.fit(inputs, labels, batch_size=batch_size, epochs=epochs, validation_split=validation_split)
        self.model.save('model.hdf5')
        self.logger.info('training took {} seconds'.format(time.time() - start))

    def predict_next_point(self, inp, blind=True):
        predicted = self.model.predict(inp).squeeze()
        return predicted

    def predict_sequence_full(self, inp, feature_indices):
        predicted = []
        for i in inp:
            predicted.append(self.predict_next_point(i, feature_indices))
        return np.array(predicted).squeeze()
