import numpy
import scipy.io
import matplotlib.pyplot

mat = scipy.io.loadmat('problem2.mat')
x_data = mat.get('x')
y_data = mat.get('y')


def partition_dataset(x, y, training_set_size):
    total_size = len(x)
    random_shuffled_index = numpy.arange(len(x))
    numpy.random.shuffle(random_shuffled_index)
    x_training_data = x[random_shuffled_index[0: training_set_size]]
    y_training_data = y[random_shuffled_index[0: training_set_size]]

    x_testing_data = x[random_shuffled_index[training_set_size: total_size + 1]]
    y_testing_data = y[random_shuffled_index[training_set_size: total_size + 1]]
    return [x_training_data, y_training_data, x_testing_data, y_testing_data]


def regularized_multivariable_linear_regression(x, y, regularized_fac):
    model = numpy.matmul(numpy.matmul(numpy.linalg.inv(numpy.matmul(x.transpose(), x) +
                                                       regularized_fac * numpy.identity(x.shape[1])),
                                      x.transpose()), y)

    training_error = (1 / (2 * len(x))) * (regularized_fac * (numpy.linalg.norm(model) ** 2) +
                                           numpy.sum(numpy.float_power(y - numpy.matmul(x, model), 2)))
    return [model, training_error]


def evaluate_model(x, y, model):
    result_y = numpy.matmul(x, model)
    test_error = (1 / (2 * len(x))) * (numpy.sum(numpy.power(y - numpy.matmul(x, model), 2)))

    return [result_y, test_error]


train_size = 350
regularized_factor = 1
[train_x, train_y, test_x, test_y] = partition_dataset(x_data, y_data, train_size)

train_error_vec = []
test_error_vec = []

best_model = []
best_reg_factor = 0
best_test_loss = numpy.inf

for reg_factor in range(0, 1001):
    [regularized_model, train_error] = regularized_multivariable_linear_regression(train_x, train_y, reg_factor)
    [predicted_y, eval_error] = evaluate_model(test_x, test_y, regularized_model)

    if eval_error < best_test_loss:
        best_reg_factor = reg_factor
        best_test_loss = eval_error
        best_model = regularized_model

    train_error_vec.append(train_error)
    test_error_vec.append(eval_error)

matplotlib.pyplot.figure(figsize=(25, 16))
matplotlib.pyplot.scatter(numpy.arange(len(train_error_vec)), train_error_vec, label='train error', marker='o')
matplotlib.pyplot.scatter(numpy.arange(len(test_error_vec)), test_error_vec, label='test error', marker='x', c='r')
matplotlib.pyplot.annotate("Best regularized factor is {}".format(best_reg_factor), xy=(best_reg_factor,
                           test_error_vec[best_reg_factor - 1]), xytext=(best_reg_factor + 10,
                           test_error_vec[best_reg_factor - 1] + 5), fontsize=20, arrowprops=dict(facecolor='yellow'))

matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')
matplotlib.pyplot.show()
