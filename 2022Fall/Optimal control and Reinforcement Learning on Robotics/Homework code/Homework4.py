import numpy as np
import matplotlib.pyplot as plt


# hint: the two functions should work for states and control vectors of arbitrary dimensions (i.e. do not hard code 4 and 2!)
# you may want to test individual functions and the whole code first on your computer for easier debugging and to find appropriate gain matrices

def solve_LQR_trajectory(A, B, Q, R, x_bar, N):
    '''
    A, B, Q and R are the matrices defining the OC problem
    x_bar is the trajectory of desired states of size dim(x) x (N+1)
    N is the horizon length

    The function returns 1) a list of gains of length N and 2) a list of feedforward controls of length N
    '''
    K_gains = []  # K_i

    list_of_P = [Q]  # P_i and P_N

    k_feedforward = []  # k_i

    list_of_p = []  # p_i
    x_bar_N = x_bar[:, N]
    qN = - Q.dot(x_bar_N)
    list_of_p.append(qN)  # p_N

    for i in range(N):
        K_i = -1 * np.linalg.inv(R + B.transpose().dot(list_of_P[i]).dot(B)).dot(B.transpose()).dot(list_of_P[i]).dot(A)

        P_i = Q + A.transpose().dot(list_of_P[i]).dot(A) + A.transpose().dot(list_of_P[i]).dot(B).dot(K_i)

        k_i = -1 * np.linalg.inv(R + B.transpose().dot(list_of_P[i]).dot(B)).dot(B.transpose()).dot(list_of_p[i])

        x_bar_i = x_bar[:, N - i - 1]
        q_i = - Q.dot(x_bar_i)
        p_i = q_i + A.transpose().dot(list_of_p[i]) + A.transpose().dot(list_of_P[i]).dot(B).dot(k_i)

        K_gains.append(K_i)
        list_of_P.append(P_i)
        k_feedforward.append(k_i)
        list_of_p.append(p_i)

    return K_gains[::-1], k_feedforward[::-1]


def simulate_dynamics(A, B, K_gains, k_feedforward, x0, N):
    '''
    A, B define the system dynamics
    K_gains is a list of feedback gains of length N
    k_feedforward is a list of feedforward controls of length N
    x0 is the initial state (array of dim (dim(state) x 1))

    The function returns 1) an array of states (dim(states) x N+1) and 2) an array of controls (dim(control) x N)
    '''
    x = np.zeros([A.shape[0], N + 1])
    u = np.zeros([B.shape[1], N])

    x[:, 0] = x0[:, 0]

    for i in range(N):
        current_state_x = x[:, i]
        optimal_control_policy = K_gains[i].dot(current_state_x) + k_feedforward[i]
        next_state = A.dot(current_state_x) + B.dot(optimal_control_policy)

        x[:, i + 1] = next_state
        u[:, i] = optimal_control_policy

    return x, u


# we generate a random initial state
x0 = np.random.uniform(-2., .2, (4, 1))

deltaT = 0.01

# we want a trajectory of 20 seconds
t = np.arange(0., 20.01, deltaT)
N = len(t) - 1

omega = 0.5 * np.pi

### WRITE CODE THAT SOLVES THE PROBLEM HERE ###
# Define A and B
A = np.array([[1, deltaT, 0, 0], [0, 1, 0, 0], [0, 0, 1, deltaT], [0, 0, 0, 1]])
B = np.array([[0, 0], [deltaT, 0], [0, 0], [0, deltaT]])

# Define Q and R
Q = 100 * np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]])
R = 0.1 * np.array([[1, 0], [0, 1]])

# Define the desired trajectory, x_bar
x_bar = np.zeros([4, N + 1])
for i in range(N + 1):
    time_stamp = t[i]
    x_state = np.array([np.sin(omega * time_stamp), omega * np.cos(omega * time_stamp),
                        np.sin(2 * omega * time_stamp), 2 * omega * np.cos(2 * omega * time_stamp)])
    x_bar[:, i] = x_state

# Calc the LQR trajectory
K_gain, k_feedforward = solve_LQR_trajectory(A, B, Q, R, x_bar, N)
x, u = simulate_dynamics(A, B, K_gain, k_feedforward, x0, N)

#### ONCE THIS IS DONE WE PLOT THE RESULTS ####
plt.figure(figsize=(25, 16))
plt.plot(x[0, :], x[2, :], x_bar[0, :], x_bar[2, :])
plt.xlabel('Position in first dimension', fontsize=20)
plt.ylabel('Position in second dimension', fontsize=20)
plt.title('Trajectory of the car in 2D', fontsize=20)
plt.legend(['simulated trajectory', 'desired'], fontsize=20)

plt.figure(figsize=(25, 16))
names = ['Pos. 1', 'Vel. 1', 'Pos. 2', 'Vel. 2']
for i in range(4):
    plt.subplot(4, 1, 1 + i)
    plt.plot(t, x[i, :], t, x_bar[i, :], '--')
    plt.ylabel(names[i], fontsize=20)
plt.xlabel('Time [s]', fontsize=20)

plt.figure(figsize=(25, 16))
plt.plot(t[:-1], u.T)
plt.legend(['Control 1', 'Control 2'], fontsize=20)
plt.xlabel('Time [s]', fontsize=20)
plt.show()
