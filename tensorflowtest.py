import random
import logging
import datetime
import numpy as np
import tensorflow as tf
import data_encoder as de


# SET LOGGING LEVELS
logging_level = logging.INFO
tf_logging_level = tf.logging.ERROR
logging.basicConfig(level=logging_level)
tf.logging.set_verbosity(tf_logging_level)

# HYPERPARAMETERS
log_every = 100
num_epochs = 100
batch_size = 512
save_every = 10000
max_steps = 100000
learning_rate = 1e-1
hidden_layer_size = 1024

# LOAD DATA
# TODO: open real text here
with open('1984.txt') as f:
    text = f.read()

# GET UNIQUES
unique_chars = sorted(list(set(text)))
vocab_size = len(unique_chars)
print('Text is {} characters long'.format(len(text)))
print('Number of unique characters in text: {}'.format(vocab_size))
# GENERATE MAPS BETWEEN TOKENS AND INDICES
index_to_token = {index: token for index, token in enumerate(unique_chars)}
token_to_index = {token: index for index, token in enumerate(unique_chars)}

# GENERATE SECTIONS AND NEXT_CHARS
len_per_section = 50
skip = 2
sections = []
next_chars = []
for i in range(0, len(text) - len_per_section, skip):
    sections.append(text[i: i + len_per_section])
    next_chars.append(text[i + len_per_section])

# GENERATE TRAINING DATA
x = np.zeros((len(sections), len_per_section, vocab_size), dtype=np.float32)
y = np.zeros((len(sections), vocab_size), dtype=np.float32)
for i, section in enumerate(sections):
    for j, char in enumerate(section):
        x[i, j, token_to_index[char]] = 1
    y[i, token_to_index[next_chars[i]]] = 1

# PROVIDE STARTING SEQUENCE
test_start = 'Winston'


# SET CHECKPOINT DIRECTORY
ckpt_dir = 'ckpt'
logging.debug('checkpoint subdirectory: {}'.format(ckpt_dir))
# CLEAR CHECKPOINT DIRECTORY
if tf.gfile.Exists(ckpt_dir):
    tf.gfile.DeleteRecursively(ckpt_dir)
    logging.info('Checkpoint directory deleted')
tf.gfile.MakeDirs(ckpt_dir)
logging.info('New checkpoint directory created')


# CREATE GRAPH
graph = tf.Graph()
with graph.as_default():
    global_step = tf.Variable(0)
    with tf.name_scope('input_data'):
        data = tf.placeholder(tf.float32, [batch_size, len_per_section, vocab_size])
        labels = tf.placeholder(tf.float32, [batch_size, vocab_size])

    with tf.name_scope('input'):
        # Input gate: weights for input, weights for previous input, bias
        w_ii = tf.Variable(tf.truncated_normal([vocab_size, hidden_layer_size], -0.1, 0.1), name='weight_in')
        w_io = tf.Variable(tf.truncated_normal([hidden_layer_size, hidden_layer_size], -0.1, 0.1), name='weight_out')
        b_i = tf.Variable(tf.zeros([1, hidden_layer_size]), name='bias')
    with tf.name_scope('forget'):
        # Forget gate
        w_fi = tf.Variable(tf.truncated_normal([vocab_size, hidden_layer_size], -0.1, 0.1), name='weight_in')  # current in weights
        w_fo = tf.Variable(tf.truncated_normal([hidden_layer_size, hidden_layer_size], -0.1, 0.1), name='weight_out')  # prev out weights
        b_f = tf.Variable(tf.zeros([1, hidden_layer_size]), name='bias')
    with tf.name_scope('output'):
        # Output gate
        w_oi = tf.Variable(tf.truncated_normal([vocab_size, hidden_layer_size], -0.1, 0.1), name='weight_in')  # current in weights
        w_oo = tf.Variable(tf.truncated_normal([hidden_layer_size, hidden_layer_size], -0.1, 0.1), name='weight_out')  # prev out weights
        b_o = tf.Variable(tf.zeros([1, hidden_layer_size]), name='bias')
    with tf.name_scope('memory'):
        # Memory Cell
        w_ci = tf.Variable(tf.truncated_normal([vocab_size, hidden_layer_size], -0.1, 0.1), name='weight_in')  # current in weights
        w_co = tf.Variable(tf.truncated_normal([hidden_layer_size, hidden_layer_size], -0.1, 0.1), name='weight_out')  # prev out weights
        b_c = tf.Variable(tf.zeros([1, hidden_layer_size]), name='bias')


    def lstm(i, o, state):
        with tf.name_scope('lstm'):
            input_gate = tf.sigmoid(tf.matmul(i, w_ii) + tf.matmul(o, w_io) + b_i)
            forget_gate = tf.sigmoid(tf.matmul(i, w_fi) + tf.matmul(o, w_fo) + b_f)
            output_gate = tf.sigmoid(tf.matmul(i, w_oi) + tf.matmul(o, w_oo) + b_o)
            memory_cell = tf.sigmoid(tf.matmul(i, w_ci) + tf.matmul(o, w_co) + b_c)
            state = input_gate * memory_cell + forget_gate * state
            output = output_gate * tf.tanh(state)

        return output, state


    # OPERATIONS
    # LSTM
    output = tf.zeros([batch_size, hidden_layer_size])
    state = tf.zeros([batch_size, hidden_layer_size])
    outputs_all_i = output
    labels_all_i = data[:, 1, :]
    for i in range(1, len_per_section):
        output, state = lstm(data[:, i, :], output, state)
        if i != len_per_section - 1:
            outputs_all_i = tf.concat([outputs_all_i, output],0 )
            labels_all_i = tf.concat([labels_all_i, data[:, i + 1, :]], 0)
        else:
            outputs_all_i = tf.concat([outputs_all_i, output], 0)
            labels_all_i = tf.concat([labels_all_i, labels], 0)

    w = tf.Variable(tf.truncated_normal([hidden_layer_size, vocab_size], -0.1, 0.1))
    b = tf.Variable(tf.zeros([vocab_size]))
    logits = tf.matmul(outputs_all_i, w) + b
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels_all_i))
    optimizer = tf.train.GradientDescentOptimizer(10.).minimize(loss, global_step=global_step)


with tf.Session(graph=graph) as sess:
    tf.global_variables_initializer()
    offset = 0
    saver = tf.train.Saver()
    for step in range(max_steps):
        offset = offset % len(x)
        # BATCHIFICATION
        if offset <= (len(x) - batch_size):
            batch_data = x[offset: offset + batch_size]
            batch_labels = y[offset: offset + batch_size]
            offset += batch_size
        else:
            to_add = batch_size - (len(x) - offset)
            batch_data = np.concatenate((x[offset: len(x)], x[0: to_add]))
            batch_labels = np.concatenate((y[offset: len(x)], y[0: to_add]))
            offset = to_add
        _, training_loss = sess.run([optimizer, loss], feed_dict={data: batch_data, labels: batch_labels})

        if step % log_every == 0:
            print('====================\nTIME: {}\nSTEP: {}\n LOSS: {}'.format(datetime.datetime.now(),
                                                                               step,
                                                                               training_loss))
        if step % save_every == 0:
            saver.save(sess, ckpt_dir + '\\model', global_step=step)

def sample(prediction):
    rand_prob = random.uniform(0, 1)
    cumulative_prob = 0
    char_idx = len(prediction) - 1
    for idx in range(len(prediction)):
        cumulative_prob += prediction[idx]
        if cumulative_prob >= rand_prob:
            char_idx = idx
            break

    char_one_hot = np.eye(vocab_size)[char_idx]
    return char_one_hot


if __name__ == '__main__':
    pass
    # with tf.Session() as sess:
    #     tf.tables_initializer().run()
    #     tf.global_variables_initializer().run()
    #     print(sess.run(one_hot))
