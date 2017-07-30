import tensorflow as tf
import numpy as np
import data_encoder as de

tf.logging.set_verbosity(tf.logging.ERROR)
data = de.data

# HYPERPARAMETERS
hidden_layer_size = 100
sequence_length = 25
learning_rate = 1e-1
echo_step = 1
num_epochs = 100
batch_size = 200
num_classes = data.vocab_size
series_length = data.data_size
truncated_backprop_length = 15
num_batches = series_length//batch_size//truncated_backprop_length

# Generate input and target data
de.one_hot_encode_tokens()
input_data = data.one_hot
target_data = np.roll(data.one_hot, -echo_step, axis=0)
target_data[-1] = 0

# MODEL PARAMETERS
# inputs to hidden layer
U = tf.Variable(tf.random_uniform((hidden_layer_size, data.vocab_size),
                                  -np.sqrt(1/hidden_layer_size),
                                  np.sqrt(1/data.vocab_size)))
# hidden to output layer
V = tf.Variable(tf.random_uniform((data.vocab_size, hidden_layer_size),
                                  -np.sqrt(1/hidden_layer_size),
                                  np.sqrt(1/hidden_layer_size)))
# hidden to hidden layer
W = tf.Variable(tf.random_uniform((hidden_layer_size, hidden_layer_size),
                                  -np.sqrt(1/hidden_layer_size),
                                  np.sqrt(1/hidden_layer_size)))
bh = tf.Variable(tf.zeros((hidden_layer_size, 1)))
by = tf.Variable(tf.zeros((data.vocab_size, 1)))


def forward_propagation(x):
    """
    Perform forward pass
    :param x: input data as a one-hot vector
    :return:
    """
    t = len(x)
    h = tf.zeros((t + 1, hidden_layer_size))  # history of hidden states
    o = tf.zeros((t, data.vocab_size))  # initialize output history
    for t in np.arange(t):
        # current_hidden = tanh(current_input + dot(W, prev_hidden) + biases)
        tf.scatter_update(h, t, tf.tanh(tf.matmul(U, x[t]) + tf.matmul(W, h[t-1]) + bh))
        tf.scatter_update(o, t, tf.nn.softmax(tf.matmul(V, h[t]) + by))
    return [o, h]


def predict(x):
    """
    :param x: input data as a one-hot vector
    :return:
    """
    o, h = forward_propagation(x)
    return np.argmax(o, axis=1)


if __name__ == '__main__':
    pass
    # with tf.Session() as sess:
    #     tf.tables_initializer().run()
    #     tf.global_variables_initializer().run()
    #     print(sess.run(one_hot))
