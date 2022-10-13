import numpy as np
import matplotlib.pyplot as plt


# a is defined a priori, you may use a = 2. to test your code
# b is defined a priori, you may use b = 10. to test your code

def get_running_cost(a, b, x, u):
    # fill this function to return the running cost

    running_cost = a * np.abs(x - 5) + b * u ** 2
    # running_cost = a * np.abs(x) + b * u ** 2
    return running_cost


def get_final_cost(x):
    # fill this function to return the final cost given x
    return 0 if x == 5 else 10000000
    # return 0 if x == -2 else 1000


def next_state(x, u):
    # fill this function to return the next state
    result = x + 0.1 * u
    if result > 5:
        result = 5
    elif result < 0:
        result = 0
    return result
    # result = x + u + 1
    # if result > 2:
    #     result = 2
    # elif result < -2:
    #     result = -2
    # return result


a = 9.4
b = 6.4
# this numpy array enumerates all possible states (assume that your cost to go will return a numpy array that follows this ordering)
possible_states = np.arange(0, 5.1, 0.1)

# this numpy array enumerates all possible control
possible_control = np.array([0, 1, 2, 3, 4, 5])


def get_cost_to_go(next_cost_to_go):
    # next_cost_to_go is a 1D numpy array of size = number of possible states
    # fill this function (and change what is returned)

    # Create empty array to store the results
    optimal_control = np.zeros_like(next_cost_to_go)
    current_cost_to_go = np.zeros_like(next_cost_to_go)

    # Get the number of the states and controls
    num_of_states = next_cost_to_go.size
    num_of_controls = possible_control.size

    for i in range(num_of_states):
        current_state = possible_states[i]
        # best_control_index = 0
        current_min_cost = np.inf

        # for each possible states, enumerate all possible next states and calculate corresponding cost
        for j in range(num_of_controls):
            control_unit = possible_control[j]
            next_state_value = next_state(current_state, control_unit)
            next_state_index = round(next_state_value * 10)
            # next_state_index = np.where(possible_states == next_state_value)[0]

            # Calculate the cost if we use the control unit to transfer to the next state
            running_cost = get_running_cost(a, b, current_state, control_unit)
            current_total_cost = next_cost_to_go[next_state_index] + running_cost

            # Try to find a minimum cost
            if current_min_cost > current_total_cost:
                best_control_index = j
                current_min_cost = current_total_cost

        # Record the best control unit and the cost_to_go for current state
        current_cost_to_go[i] = current_min_cost
        optimal_control[i] = possible_control[best_control_index]

    return current_cost_to_go, optimal_control


# J_cost_to_go = np.array(
#     [1.82548534, 41.66116738, 12.73256244, 72.85341084, 62.66438975, 1.76327703, 35.57717707, 6.08681015, 96.97241448, 54.71315854, 53.91469635,
#      53.43741831, 56.36345727, 5.6606026, 71.60908449, 78.69612352, 62.75546361, 32.45869043, 5.78078294, 13.34745165, 32.41431504, 52.59973959,
#      4.68068169, 39.20355336, 24.37416888, 43.69373308, 91.21752957, 93.22747671, 45.0070959, 82.8219011, 1.09754396, 7.60874682, 1.72304357,
#      25.10140111, 56.80457196, 59.88090675, 98.57930087, 40.38896414, 86.31742433, 98.47935792, 41.70376821, 1.48501627, 12.93415824, 39.43222623,
#      28.71800851, 79.77742907, 34.04131222, 16.18943841, 80.01267704, 45.30527858, 56.37499978])
# a = 73
# b = 28.9
#
# test_cost_to_go, test_optimal_control = get_cost_to_go(J_cost_to_go)


a = 9.4
b = 6.4
# this numpy array enumerates all possible states (assume that your cost to go will return a numpy array that follows this ordering)
# possible_states = np.arange(-2, 3, 1)
#
# # this numpy array enumerates all possible control
# possible_control = np.array([-1, 0, 1])

N = 29
# a = 10
# b = 10
number_of_states = possible_states.size

# outputs
cost_to_go = np.zeros([number_of_states, N + 1])  # cost_to_go matrix, each column represents a stage
control_law_mat = np.zeros([number_of_states, N])  # control unit matrix, each column represents a stage

# Calculate final cost_to_go
for i in range(number_of_states):
    cost_to_go[i, N] = get_final_cost(possible_states[i])

for i in range(N - 1, -1, -1):
    # get cost_to_go of next state (x_{n+1})
    J_n_plus_1 = cost_to_go[:, i + 1]
    # calculate the optimal cost and control unit for current state (x_n)
    cost_to_go_n, optimal_control_unit_n = get_cost_to_go(J_n_plus_1)

    # store the result
    cost_to_go[:, i] = cost_to_go_n
    control_law_mat[:, i] = optimal_control_unit_n

x = np.zeros(N + 1)  # sequence of states
u = np.zeros(N)  # sequence of optimal control units
J_best_cost = cost_to_go[0, 0]  # best cost, is the min value in the first column

for i in range(N):
    #  get current state
    state_x_n = x[i]
    current_index = round(state_x_n * 10)
    # current_index = np.where(possible_states == state_x_n)[0]
    # current_index = int(state_x_n + 2)

    u[i] = control_law_mat[current_index, i]
    x[i + 1] = next_state(x[i], u[i])

plt.figure()
plt.subplot(2,1,1)
plt.plot(x, '-o')
plt.ylabel('State')
plt.subplot(2,1,2)
plt.plot(u, '-o')
plt.ylabel('Control')
plt.xlabel('Stages')
plt.show()
