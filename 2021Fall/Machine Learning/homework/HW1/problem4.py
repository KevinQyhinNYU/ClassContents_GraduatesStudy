import numpy
import scipy.io
import matplotlib.pyplot

mat = scipy.io.loadmat('dataset4.mat')
x_data = mat.get('X')
y_data = mat.get('Y')


def partition_dataset(x, y, training_set_size):
    total_size = len(x)
    x_training_data = x[0: training_set_size]
    y_training_data = y[0: training_set_size]

    x_testing_data = x[training_set_size: total_size + 1]
    y_testing_data = y[training_set_size: total_size + 1]
    return [x_training_data, y_training_data, x_testing_data, y_testing_data]


def sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


def calc_loss(x, y, theta):
    # add a trivial value to avoid computing log(0)
    epsilon = 1e-6
    h = sigmoid(numpy.matmul(x, theta))
    cost = (-1 / len(y)) * (numpy.matmul(y.transpose(), numpy.log(h + epsilon)) +
                            numpy.matmul((1 - y).transpose(), numpy.log(h + epsilon)))
    return cost[0, 0]


def gradient_descent(x, y, theta, learning_rate, tolerance):
    loss_list = []
    n = len(y)

    last_theta = numpy.ones(theta.shape)
    iteration = 10000
    # while numpy.linalg.norm(theta - last_theta, ord=1) >= tolerance:
    #     if iteration != 1:
    #         last_theta = theta
    #     theta = theta - (learning_rate / n) * numpy.matmul(x.transpose(), (sigmoid(numpy.matmul(x, theta)) - y))
    #     loss = calc_loss(x, y, theta)
    #     loss_list.append(loss)
    #     iteration = iteration + 1
    for i in range(iteration):
        theta = theta + (learning_rate / n) * numpy.matmul(x.transpose(), (sigmoid(numpy.matmul(x, theta)) - y))
        loss = calc_loss(x, y, theta)
        loss_list.append(loss)
    return [theta, loss_list]


train_size = 100
[x_train, y_train, x_test, y_test] = partition_dataset(x_data, y_data, train_size)

lr = 0.01
margin = 0.001
params = numpy.random.rand(x_train.shape[1], 1)
[params, loss_stat] = gradient_descent(x_data, y_data, params, lr, margin)

print("model is: \n", params)
matplotlib.pyplot.plot(list(range(len(loss_stat))), loss_stat, label='train loss')
matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')
matplotlib.pyplot.show()
