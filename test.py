import numpy as np
from trumpreader import data, tokens
import time

# data = open('data.txt', 'r').read()
chars = sorted(set(tokens))
data_size, vocab_size = len(data), len(chars)
# print('data has {}, {} unique'.format(data_size, vocab_size))
char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}

# HYPERPARAMETERS
HIDDEN_SIZE = 100
seq_length = 140
LEARNING_RATE = 1e-1


# MODEL PARAMETERS
# weights from input to hidden
Wxh = np.random.uniform(-1/np.sqrt(vocab_size), 1/np.sqrt(vocab_size), (HIDDEN_SIZE, vocab_size))
# weights from hidden to hidden
Whh = np.random.uniform(-1/np.sqrt(HIDDEN_SIZE), 1/np.sqrt(HIDDEN_SIZE), (HIDDEN_SIZE, HIDDEN_SIZE))
# weights from hidden to output
Why = np.random.uniform(-1/np.sqrt(HIDDEN_SIZE), 1/np.sqrt(HIDDEN_SIZE), (vocab_size, HIDDEN_SIZE))
# biases
bh = np.zeros((HIDDEN_SIZE, 1))
by = np.zeros((vocab_size, 1))


def loss_function(inputs, targets, hprev):
    xs, hs, ys, ps = {}, {}, {}, {}
    # copy previous hidden state
    hs[-1] = np.copy(hprev)

    loss = 0

    # FORWARD PASS
    for t in range(len(inputs) - 1):
        # one-hot encode
        xs[t] = np.zeros((vocab_size, 1))
        xs[t][inputs[t]] = 1  # set correct index to 1 using integer from 'inputs'

        # hidden state
        hs[t] = np.tanh(np.dot(Wxh, xs[t]) + np.dot(Whh, hs[t-1]) + bh)
        # unnormalized log probabilities for output
        ys[t] = np.dot(Why, hs[t]) + by
        # normalized probabilities for output
        ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t]))
        loss += -np.log(ps[t][targets[t], 0])  # softmax (cross-entropy loss)

    # BACKWARD PASS
    # initialize gradients
    dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
    dbh, dby = np.zeros_like(bh), np.zeros_like(by)
    # next hidden state
    dhnext = np.zeros_like(hs[0])

    for t in reversed(range(len(inputs) - 1)):
        dy = np.copy(ps[t])  # output probabilities
        # derive first gradient
        dy[targets[t]] -= 1  # backprop into y
        dWhy += np.dot(dy, hs[t].T)
        dby += dy
        # backpropagate!
        dh = np.dot(Why.T, dy) + dhnext  # backprop into h
        dhraw = (1 - hs[t] * hs[t]) * dh  # backprop through tanh nonlinearity
        dbh += dhraw  # derivative of hidden bias
        dWxh += np.dot(dhraw, xs[t].T)  # derivative of input to hidden layer weight
        dWhh += np.dot(dhraw, hs[t-1].T)  # derivative of hidden layer to hidden layer weight
        dhnext = np.dot(Whh.T, dhraw)

    for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
        np.clip(dparam, -5, 5, out=dparam)  # clip to mitigate exploding gradients

    return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs) - 2]


def sample(h, seed_ix, n):
    """
    output a sample sequence of integers from the model

    h = memory state
    seed_ix = seed letter from first timestep
    n = how many characters to output
    """

    # create vector
    x = np.zeros((vocab_size, 1))
    x[seed_ix] = 1
    ixes = []

    for t in range(n):
        h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h) + bh)
        y = np.dot(Why, h) + by
        p = np.exp(y) / np.sum(np.exp(y))  # normalized probabilities
        ix = np.random.choice(range(vocab_size), p=p.ravel())  # pick the one with the highest probability
        x = np.zeros((vocab_size, 1))
        x[ix] = 1
        ixes.append(ix)

    txt = ' '.join(ix_to_char[i] for i in ixes)
    return '----\n {0} \n----'.format(txt)

start_time = time.clock()
n = 0
mWxh, mWhh, mWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
mbh, mby = np.zeros_like(bh), np.zeros_like(by)

smooth_loss = -np.log(1.0/vocab_size)  # initial loss

while n >= 0:
    for tweet in data:
        if n == 0:
            hprev = np.zeros((HIDDEN_SIZE, 1))

        inputs = [char_to_ix[ch] for ch in tweet]
        targets = [char_to_ix[ch] for ch in (tweet[1:])]
        loss, dWxh, dWhh, dWhy, dbh, dby, hprev = loss_function(inputs, targets, hprev)
        smooth_loss = smooth_loss * 0.999 + loss * 0.001

        if n % 10 == 0:
            print('iteration {0}, loss = {1}'.format(n, smooth_loss))
            print('time elapsed:', time.clock() - start_time, 'seconds.')
            print(sample(hprev, inputs[0], 20))

        # update via adagrad
        for param, dparam, mem in zip([Wxh, Whh, Why, bh, by],
                                      [dWxh, dWhh, dWhy, dbh, dby],
                                      [mWxh, mWhh, mWhy, mbh, mby]):
            mem += dparam * dparam
            param += -LEARNING_RATE * dparam / np.sqrt(mem + 1e-8)

        n += 1
