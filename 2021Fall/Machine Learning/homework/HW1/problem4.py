import numpy
import scipy.io
import matplotlib.pyplot

mat = scipy.io.loadmat('dataset4.mat')
x_data = mat.get('X')
y_data = mat.get('Y')


# 1.Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


# 2.Calculating loss
def calc_loss(x, y, theta):
    h = sigmoid(numpy.matmul(x, theta))
    cost = -(1 / len(y)) * (numpy.matmul((y - 1).transpose(), numpy.log(1 - h + 1e-6)) -
                            numpy.matmul(y.transpose(), numpy.log(h + 1e-6)))
    return cost[0, 0]


# 3.Gradient descent
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

        distances = (numpy.matmul(x, theta) > 0).astype(numpy.int64)
        classification_error_cnt = (numpy.linalg.norm(y - distances, ord=1)).astype(numpy.int64)
        classification_error_list.append(classification_error_cnt)

        loss = calc_loss(x, y, theta)
        loss_list.append(loss)
        iteration = iteration + 1
    return [theta, loss_list, iteration, classification_error_list]


lr = 1
margin = 0.001
params = numpy.random.rand(x_data.shape[1], 1)
[params, loss_stat, iter_nums, classify_stat] = gradient_descent(x_data, y_data, params, lr, margin)

# 4.Plot the results

matplotlib.pyplot.figure(figsize=(25, 16))
matplotlib.pyplot.subplot(1, 2, 1)
matplotlib.pyplot.plot(list(range(len(loss_stat))), loss_stat, label='Training loss')
matplotlib.pyplot.plot(list(range(len(classify_stat))), classify_stat, label='Binary classification error')
matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')
matplotlib.pyplot.title("Training loss and Binary classification error", fontsize=10)

matplotlib.pyplot.subplot(1, 2, 2)
x_positive = []
y_positive = []
x_negative = []
y_negative = []

for i in range(len(x_data)):
    if y_data[i, 0] > 0:
        x_positive.append(x_data[i, 0])
        y_positive.append(x_data[i, 1])
    else:
        x_negative.append(x_data[i, 0])
        y_negative.append(x_data[i, 1])

matplotlib.pyplot.scatter(x_positive, y_positive, marker='o', c='r', label='Positive items')
matplotlib.pyplot.scatter(x_negative, y_negative, marker='x', c='b', label='Negative items')

t_series = numpy.arange(0, 1, 0.01).tolist()
ft_list = []
for t in t_series:
    ft_list.append(-(params[0] * t + params[2]) / params[1])
matplotlib.pyplot.plot(t_series, ft_list, c='k', label='Boundary line')

dist_sign = (numpy.matmul(x_data, params) > 0).astype(numpy.int64)
classify_error_cnt = numpy.linalg.norm(y_data - dist_sign, ord=1).astype(numpy.int64)
matplotlib.pyplot.title("Classification Error Number is: {}\n Logistic Classification Boundary line is shown "
                        "below".format(classify_error_cnt), fontsize=10)

info_str = "Learning rate is: {}, Tolerance is: {} \nTotal iteration num is: {}\n Params are: [{:.3f}, {:.3f}, {:.3f}]" \
    .format(lr, margin, iter_nums,
            params[0, 0],
            params[1, 0],
            params[2, 0])
matplotlib.pyplot.suptitle(info_str, fontsize=10)

matplotlib.pyplot.legend(fontsize='large', loc='upper right')
matplotlib.pyplot.show()
