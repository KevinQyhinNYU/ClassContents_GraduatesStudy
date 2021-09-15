import numpy
import scipy.io
import matplotlib.pyplot

# load the data needed
mat = scipy.io.loadmat("problem1.mat")
x_data = mat.get('x')
y_data = mat.get('y')
order = 10
# modelOrder = numpy.random(0, 10)
# initialize X matrix

print(len(mat['x']))
print(type(mat['x']))

xx = numpy.zeros((x_data.shape[0], order))
print(xx.shape)
for i in range(1, order):
    # print(type(xx[:, i]))
    print(xx[:, i].shape)
    print(xx[:, i])
    tmpCol = numpy.power(x_data, order - i)[:, 0]
    xx[:, i] = tmpCol
print(xx)

print(numpy.linalg.pinv(xx).shape)
model = numpy.matmul(numpy.linalg.pinv(xx), y_data)
print("The model is: \n", model)
training_error = (1 / (2 * len(x_data))) * numpy.sum(numpy.power(y_data - numpy.matmul(xx, model), 2))
print("Training error is: \n", training_error)

# x_axis_data = numpy.linspace(1, 500, 500, endpoint=True)
# x_axis_data.resize(500, 1)
# print(type(x_axis_data))
# print(x_axis_data.shape)

# plot the results
print(x_data.shape)
matplotlib.pyplot.figure(figsize=(16, 9))
matplotlib.pyplot.scatter(x_data[1:100], y_data[1:100], label='nonlinear', marker='o')
matplotlib.pyplot.legend(loc='upper right')

matplotlib.pyplot.show()
