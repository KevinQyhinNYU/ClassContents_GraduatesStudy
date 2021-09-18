import numpy
import scipy.io
import matplotlib.pyplot

mat = scipy.io.loadmat('dataset4.mat')
x_data = mat.get('X')
y_data = mat.get('Y')


def sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


def calc_loss(x, y, theta):
    h = sigmoid(numpy.matmul(x, theta))
    cost = -(1 / len(y)) * (numpy.matmul((y - 1).transpose(), numpy.log(1 - h + 1e-6)) -
                            numpy.matmul(y.transpose(), numpy.log(h + 1e-6)))
    return cost[0, 0]


def gradient_descent(x, y, theta, learning_rate, tolerance):
    loss_list = []
    classification_error_list = []
    n = len(y)

    last_theta = theta - 1
    iteration = 1
    while numpy.linalg.norm(theta - last_theta, ord=1) >= tolerance:
        if iteration != 1:
            last_theta = theta
        theta = theta - (learning_rate / n) * numpy.matmul(x.transpose(), (sigmoid(numpy.matmul(x, theta)) - y))
        #
        # classification_error_cnt = 0
        # for i in range(len(x)):
        #     ptxx = x[i, :]
        #     ptxx = numpy.resize(ptxx, (3, 1))
        #     distance = numpy.matmul(params.T, ptxx)
        #     if distance > 0:
        #         if y_data[i] != 1:
        #             classification_error_cnt = classification_error_cnt + 1
        #     else:
        #         if y_data[i] != 0:
        #             classification_error_cnt = classification_error_cnt + 1
        #
        # (numpy.matmul(x, theta) > 0) - y
        # classification_error_list.append(classification_error_cnt)

        loss = calc_loss(x, y, theta)
        loss_list.append(loss)
        iteration = iteration + 1
    return [theta, loss_list, iteration, classification_error_list]


lr = 0.5
margin = 0.002
params = numpy.random.rand(x_data.shape[1], 1)
[params, loss_stat, iter_nums, classify_stat] = gradient_descent(x_data, y_data, params, lr, margin)

print("model is: \n", params)
print("Number of iterations to converge: \n", iter_nums)
matplotlib.pyplot.subplot(1, 2, 1)
matplotlib.pyplot.plot(list(range(len(loss_stat))), loss_stat, label='train loss')
matplotlib.pyplot.plot(list(range(len(classify_stat))), classify_stat, label='classification error')
matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')

matplotlib.pyplot.subplot(1, 2, 2)
x_positive = []
y_positive = []
x_negative = []
y_negative = []

classify_error_cnt = 0

for i in range(len(x_data)):
    ptx = x_data[i, :]
    ptx = numpy.resize(ptx, (3, 1))
    dist = numpy.matmul(params.T, ptx)
    if dist > 0:
        x_positive.append(x_data[i, 0])
        y_positive.append(x_data[i, 1])
        if y_data[i] != 1:
            classify_error_cnt = classify_error_cnt + 1
    else:
        x_negative.append(x_data[i, 0])
        y_negative.append(x_data[i, 1])
        if y_data[i] != 0:
            classify_error_cnt = classify_error_cnt + 1

print("Total misclassification num: \n", classify_error_cnt)
matplotlib.pyplot.scatter(x_positive, y_positive, marker='o', c='r', label='positive items')
matplotlib.pyplot.scatter(x_negative, y_negative, marker='x', c='b', label='negative items')

t_series = numpy.arange(0, 1, 0.01).tolist()
ft_list = []
for t in t_series:
    ft_list.append(-(params[0] * t + params[2]) / params[1])
matplotlib.pyplot.plot(t_series, ft_list, c='k', label='boundary line')

matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')
matplotlib.pyplot.show()
