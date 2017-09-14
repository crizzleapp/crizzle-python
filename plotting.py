import matplotlib.pyplot as plt
import preprocessing as pp


# region Plotting Functions
def plot_results(predicted_data, full_dataset, fraction):
    true_data = pp.train_test_split(full_dataset, fraction)
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
    true_data = pp.train_test_split(full_dataset, fraction)
    xs = range(len(full_dataset))
    fig = plt.figure(facecolor='white', figsize=(8, 5))
    ax = fig.add_subplot(111)
    ax.plot(xs[:len(true_data[2])], true_data[2][:, 0], label='Train Data')
    ax.plot(xs[len(true_data[2]):], true_data[3][:, 0], label='Test Data')
    plt.scatter(0, 0, label='Prediction', c='g', s=1)
    plt.legend()
    plt.pause(0.01)
    return xs, ax, len(true_data[2])


def freeze_plot():
    plt.ioff()
    plt.show()


def update_plot(predicted_data, index):
    # print('index: {}, prediction: {}'.format(index, predicted_data))
    plt.scatter(index, predicted_data, c='g', s=1)
    plt.pause(0.1)
# endregion

