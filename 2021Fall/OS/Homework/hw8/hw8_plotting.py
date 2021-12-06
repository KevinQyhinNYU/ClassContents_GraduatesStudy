import numpy as np
import matplotlib.pyplot as plt

plot_nums = np.loadtxt("./lab8_result.txt")
length = plot_nums.shape[0]

plt.figure(figsize=(25, 16))
x_list = np.arange(length) + 4
plt.plot(x_list, plot_nums, marker='o')

plt.xticks(x_list, fontsize=20)
plt.xlabel("Number of frames allocated", fontsize=20)

plt.yticks(fontsize=20)
plt.ylabel("Number of Page faults", fontsize=20)

plt.show()
