from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils import plot_model
from keras.models import Sequential, load_model
import numpy as np
import logging
import time

logger = logging.getLogger(__name__)


# TODO: implement many-to-many prediction

class Predictor:
    """
    Keras-based price predictor
    """
    def __init__(self, sequence_length: int, from_disk: bool=False, filename=None):
        self.sequence_length = sequence_length
        self.from_disk = from_disk
        self.filename = filename
        self.model = None

        if from_disk:
            try:
                self.load_model_from_disk(filename)
            except OSError as e:
                logger.error('INVALID FILENAME')
                raise e
        else:
            self.build(self.sequence_length)
        self.plot_model()

    def load_model_from_disk(self, filename: str) -> None:
        self.model = load_model(filename)
        logger.info('Loaded model from disk.')

    def build(self, seqlen: int) -> None:
        """
        Build prediction model

        Args:
            seqlen (int): length of input/output sequences in data
        """
        model = Sequential()
        model.add(LSTM(seqlen, input_shape=(1, seqlen),
                       return_sequences=True))

        start_time = time.clock()
        model.compile(loss='mse', optimizer='rmsprop')
        logger.info('Model built successfully.')
        logger.debug('Build time: {}'.format(time.clock() - start_time))
        self.model = model

    def plot_model(self):
        try:
            plot_model(self.model, show_shapes=True)
            logger.debug('Saved graph to image.')
        except ImportError:
            logger.error('''Error saving graph to image.
            Make sure you have correctly installed the Graphviz executables and PyDot.''')

    def train(self, inputs, labels, batch_size=256, epochs=1, validation_split=0.1):
        start = time.time()
        self.model.fit(inputs, labels, batch_size=batch_size, epochs=epochs, validation_split=validation_split)
        self.model.save('model.hdf5')
        logger.info('Model saved to disk.')
        logger.info('training took {} seconds'.format(time.time() - start))

    def predict_next(self, inp):
        predicted = self.model.predict(inp, batch_size=256).squeeze()
        return predicted

    def predict_sequence_full(self, inp):
        predicted = []
        for i in inp:
            predicted.append(self.predict_next(i))
        return np.array(predicted).squeeze()
