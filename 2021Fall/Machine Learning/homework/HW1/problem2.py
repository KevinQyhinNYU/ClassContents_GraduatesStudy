import numpy
import scipy.io
import matplotlib.pyplot

mat = scipy.io.loadmat('problem2.mat')
x_data = mat.get('x')
y_data = mat.get('y')


def partition_dataset(x, y, training_set_size):
    total_size = len(x)
    x_training_data = x[0: training_set_size]
    y_training_data = y[0: training_set_size]

    x_testing_data = x[training_set_size: total_size + 1]
    y_testing_data = y[training_set_size: total_size + 1]
    return [x_training_data, y_training_data, x_testing_data, y_testing_data]


def regularized_multivariable_linear_regression(x, y, reg_factor):
    model = numpy.matmul(numpy.matmul(numpy.linalg.inv(numpy.matmul(x.transpose(), x) +
                                                       reg_factor * numpy.identity(x.shape[1])),
                         x.transpose()), y)

    training_error = (1 / (2 * len(x))) * (reg_factor * (numpy.linalg.norm(model) ** 2) +
                                           numpy.sum(numpy.float_power(y - numpy.matmul(x, model), 2)))
    return [model, training_error]


def evaluate_model(x, y, model):
    result_y = numpy.matmul(x, model)
    test_error = (1 / (2 * len(x))) * (numpy.sum(numpy.power(y - numpy.matmul(x, model), 2)))

    return [result_y, test_error]


def display_results(y, yy):
    matplotlib.pyplot.figure(figsize=(25, 16))

    matplotlib.pyplot.scatter(numpy.arange(len(y)), y, label='train error', marker='o')
    matplotlib.pyplot.scatter(numpy.arange(len(yy)), yy, label='test error', marker='x', c='r')


train_size = 350
regularized_factor = 1
[train_x, train_y, test_x, test_y] = partition_dataset(x_data, y_data, train_size)
# [regularized_model, train_error] = regularized_multivariable_linear_regression(train_x, train_y, regularized_factor)
# [predicted_y, eval_error] = evaluate_model(test_x, test_y, regularized_model)

train_error_vec = []
test_error_vec = []

for reg_factor in range(0, 1001):
    [regularized_model, train_error] = regularized_multivariable_linear_regression(train_x, train_y, reg_factor)
    [predicted_y, eval_error] = evaluate_model(test_x, test_y, regularized_model)

    train_error_vec.append(train_error)
    test_error_vec.append(eval_error)


# print("The model is: \n", regularized_model)
# print("Training error is: \n", train_error)
# print("testing Error is: \n", eval_error)

# display_results(test_y, predicted_y)
train_error_vec.reverse()
test_error_vec.reverse()

display_results(train_error_vec, test_error_vec)
matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')
matplotlib.pyplot.show()
