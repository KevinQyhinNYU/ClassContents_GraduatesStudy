import numpy
import scipy.io
import matplotlib.pyplot

# import random

# load the data needed
mat = scipy.io.loadmat("problem1.mat")
x_data = mat.get('x')
y_data = mat.get('y')
train_set_size = 400
polynomial_order = 12


# 1.Partition the original dataset


def partition_dataset(x,
                      y,
                      training_set_size):
    total_size = len(x)
    random_shuffled_index = numpy.arange(len(x))
    numpy.random.shuffle(random_shuffled_index)
    x_training_data = x[random_shuffled_index[0: training_set_size]]
    y_training_data = y[random_shuffled_index[0: training_set_size]]
    # x_training_data = x[0: training_set_size]
    # y_training_data = y[0: training_set_size]

    x_testing_data = x[random_shuffled_index[training_set_size: total_size + 1]]
    y_testing_data = y[random_shuffled_index[training_set_size: total_size + 1]]
    # x_testing_data = x[training_set_size: total_size + 1]
    # y_testing_data = y[training_set_size: total_size + 1]
    return [x_training_data, y_training_data, x_testing_data, y_testing_data]


# 2.Compute the model from the training dataset
def polynomial_regression(x,
                          y,
                          order_num):
    xx = numpy.zeros((x.shape[0], order_num))
    for order in range(0, order_num):
        xx[:, order] = numpy.float_power(x, order_num - order - 1)[:, 0]

    model_coefficients = numpy.matmul(numpy.linalg.pinv(xx), y)
    train_error = (1 / (2 * len(x))) * numpy.sum(numpy.float_power(y - numpy.matmul(xx, model_coefficients), 2))
    return [model_coefficients, train_error]


# 3.Evaluating on the testing dataset
def evaluate_regression_model(x_test, y_test, test_model):
    total_order = len(test_model)
    xx_test = numpy.zeros((len(x_test), total_order))
    for i in range(0, total_order):
        xx_test[:, i] = numpy.float_power(x_test, total_order - i - 1)[:, 0]

    y_model = numpy.matmul(xx_test, test_model)
    testing_error = (1 / (2 * len(x_test))) * numpy.sum(numpy.power(y_test - numpy.matmul(xx_test, test_model), 2))
    return [y_model, testing_error]


# 4.Display results
def display_results(x_test, y_test, x_model, y_model):
    matplotlib.pyplot.figure(figsize=(25, 16))

    matplotlib.pyplot.scatter(x_test, y_test, label='test data', marker='o')
    matplotlib.pyplot.scatter(x_model, y_model, label='model generated data')


[x_train_data, y_train_data, x_test_data, y_test_data] = partition_dataset(x_data, y_data, train_set_size)
[model, training_error] = polynomial_regression(x_train_data, y_train_data, polynomial_order)

print("The model is: \n", model)
print("Training error is: \n", training_error)

[test_y, test_error] = evaluate_regression_model(x_test_data, y_test_data, model)
print("testing Error is: \n", test_error)

# display_results(x_test_data, y_test_data, x_test_data, test_y)

order_upper_bound = 50
train_loss = []
test_loss = []
for orders in range(1, order_upper_bound + 1):
    [new_model, new_train_error] = polynomial_regression(x_train_data, y_train_data, orders)
    [new_test_y, new_test_error] = evaluate_regression_model(x_test_data, y_test_data, new_model)
    train_loss.append(new_train_error)
    test_loss.append(new_test_error)

t_series = numpy.array(range(len(train_loss)))
tmp_trainloss = numpy.resize(numpy.array(train_loss), (len(train_loss, )))
tmp_testloss = numpy.resize(numpy.array(test_loss), (len(test_loss, )))

# matplotlib.pyplot.plot(train_loss, 'r', label='train loss')
# matplotlib.pyplot.plot(test_loss, 'b', label='test loss')

matplotlib.pyplot.plot(range(len(train_loss)), tmp_trainloss, c='r', label='train loss')
matplotlib.pyplot.plot(range(len(train_loss)), tmp_testloss, c='b', label='test loss')

matplotlib.pyplot.legend(fontsize='xx-large', loc='upper right')
matplotlib.pyplot.grid()
matplotlib.pyplot.show()
# test_xxx = numpy.arange(-50, 51)
# test_xxx = numpy.resize(test_xxx, (test_xxx.shape[0], 1))
# test_yyy = numpy.polyval(model, test_xxx)
# matplotlib.pyplot.plot(test_xxx, test_yyy, label='model generated data', color='g', linewidth=5)
# matplotlib.pyplot.show()

