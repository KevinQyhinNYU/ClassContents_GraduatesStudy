import numpy as np
import scipy.io
import matplotlib.pyplot as mplt

mat = scipy.io.loadmat('data3.mat')
data = mat.get('data')
x_data = data[:, 0: 2]
y_data = data[:, 2]
y_data = np.resize(y_data, (len(y_data), 1))


# The Signal Function
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


# Calculate the classification error and perceptron error
def calc_loss(x, y, theta, bias):
    classification_error = 0
    perceptron_error = 0
    gradient_theta = 0
    gradient_bias = 0
    n = len(y)

    for k in range(len(y)):
        x_example = x[k, :]
        x_example = np.resize(x_example, (len(x_example), 1))
        mult_val = np.matmul(theta.transpose(), x_example)
        if sign(mult_val + bias) != y[k]:
            classification_error = classification_error + 1
            perceptron_error = perceptron_error + y[k] * mult_val
            gradient_theta = gradient_theta + y[k] * x_example
            gradient_bias = gradient_bias + y[k]

    perceptron_error = -1 * perceptron_error / n
    gradient_theta = -1 * gradient_theta / n
    gradient_bias = -1 * gradient_bias / n
    return [classification_error, perceptron_error, gradient_theta, gradient_bias]


# Gradient descent process
def gradient_descent(x, y, theta, bias, learning_rate):
    perceptron_loss_list = []
    classification_error_list = []
    [classification_error, perceptron_error, gradient_theta, gradient_bias] = calc_loss(x, y, theta, bias)
    classification_error_list.append(classification_error)
    perceptron_loss_list.append(np.sum(perceptron_error))

    iteration = 1
    while classification_error != 0:
        theta = theta - learning_rate * gradient_theta
        bias = bias - learning_rate * gradient_bias
        [classification_error, perceptron_error, gradient_theta, gradient_bias] = calc_loss(x, y, theta, bias)
        classification_error_list.append(classification_error)
        perceptron_loss_list.append(np.sum(perceptron_error))
        iteration = iteration + 1

    return [theta, bias, iteration, classification_error_list, perceptron_loss_list]


def stochastic_gradient_descent(x, y, theta, bias, learning_rate):
    perceptron_loss_list = []
    classification_error_list = []

    [classification_error, perceptron_error] = calc_loss(x, y, theta, bias)
    classification_error_list.append(classification_error)
    perceptron_loss_list.append(np.sum(perceptron_error))
    gradient_theta = 0
    gradient_bias = 0
    iteration = 1

    while classification_error != 0:
        for k in range(len(y)):
            x_example = x[k, :]
            x_example = np.resize(x_example, (len(x_example), 1))
            mult_val = np.matmul(theta.transpose(), x_example)
            if sign(mult_val + bias) != y[k]:
                gradient_theta = -y[k] * x_example
                gradient_bias = -y[k]
                break

        theta = theta - learning_rate * gradient_theta
        bias = bias - learning_rate * gradient_bias
        iteration = iteration + 1
        [classification_error, perceptron_error] = calc_loss(x, y, theta, bias)
        classification_error_list.append(classification_error)
        perceptron_loss_list.append(np.sum(perceptron_error))

    return [theta, bias, iteration, classification_error_list, perceptron_loss_list]


theta_param = np.random.rand(x_data.shape[1], 1)
bias_param = np.random.rand(1, 1)
lr = 0.001
[theta_param, bias_param, iter_num, classification_loss, perceptron_loss] = gradient_descent(x_data, y_data,
                                                                                             theta_param,
                                                                                             bias_param, lr)

theta2 = np.random.rand(x_data.shape[1], 1)
bias2 = np.random.rand(1, 1)
lr2 = 0.01
[theta2, bias2, iter_num2, classification_loss2, perceptron_loss2] = gradient_descent(x_data, y_data,
                                                                                      theta2,
                                                                                      bias2, lr2)

x_positive = []
y_positive = []
x_negative = []
y_negative = []

for i in range(0, x_data.shape[0]):
    if y_data[i] == 1:
        x_positive.append(x_data[i, 0])
        y_positive.append(x_data[i, 1])
    else:
        x_negative.append(x_data[i, 0])
        y_negative.append(x_data[i, 1])

mplt.figure(figsize=(25, 16))

ax1 = mplt.subplot(1, 3, 1)
ax2 = ax1.twinx()
label1 = ax1.plot(list(range(len(classification_loss))), classification_loss, label='Classification Error', color='r')
label2 = ax2.plot(list(range(len(perceptron_loss))), perceptron_loss, label='Perceptron Error', color='k')

ax1.set_ylabel('Classification Error', fontsize=20)
ax2.set_ylabel('Perceptron Error', fontsize=20)

label = label1 + label2
label_params = [l.get_label() for l in label]

ax1.legend(label, label_params, fontsize='xx-large', loc='upper right')
info_str = "Training loss and Binary classification error (With GD) \n Learning rate is: {}, Total iteration num is: " \
           "{}\n" .format(lr, iter_num)
mplt.title(info_str, fontsize=20)

ax3 = mplt.subplot(1, 3, 2)
ax4 = ax3.twinx()
label3 = ax3.plot(list(range(len(classification_loss2))), classification_loss2, label='Classification Error', color='r')
label4 = ax4.plot(list(range(len(perceptron_loss2))), perceptron_loss2, label='Perceptron Error', color='k')

ax3.set_ylabel('Classification Error', fontsize=20)
ax4.set_ylabel('Perceptron Error', fontsize=20)

label5 = label3 + label4
label_params2 = [l.get_label() for l in label5]
ax3.legend(label5, label_params2, fontsize='xx-large', loc='upper right')
info_str2 = "Training loss and Binary classification error (With SGD) \n Learning rate is: {}, Total iteration num " \
            "is: {}\n" .format(lr2, iter_num2)
mplt.title(info_str2, fontsize=20)

mplt.subplot(1, 3, 3)
mplt.scatter(x_positive, y_positive, marker='*', c='red', label='Positive example')
mplt.scatter(x_negative, y_negative, marker='x', c='blue', label='Negative example')

t_series = np.arange(0, 1, 0.01).tolist()
ft_list = []
for t in t_series:
    ft_list.append(-(theta_param[0] * t + bias_param[0]) / theta_param[1])
mplt.plot(t_series, ft_list, c='k', label='Boundary line (with GD)')

mplt.legend(fontsize='xx-large', loc='upper right')

t_series = np.arange(0, 1, 0.01).tolist()
ft_list = []
for t in t_series:
    ft_list.append(-(theta2[0] * t + bias2[0]) / theta2[1])
mplt.plot(t_series, ft_list, c='g', label='Boundary line (with SGD)')

mplt.legend(fontsize='xx-large', loc='upper right')

mplt.show()
