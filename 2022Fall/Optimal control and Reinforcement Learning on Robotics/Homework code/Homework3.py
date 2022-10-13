# Problem 1 - Stability
# A discrete system x_{n+1} = A * x_n is stable if.f. all eigenvalues of A has norm < 1
import numpy as np


def check_stable(A):
    return np.all(np.absolute(np.linalg.eigvals(A)) < 1)


# A1 = np.array([[-0.3622, 0.3787, 0.8480, 0.0172], [-0.0897, -0.8510, -0.2338, -0.7561], [0.5324, 0.6347, -0.8312, 0.1250], [-0.4494, -0.7821, -0.2437, -0.9750]])
# A2 = np.array([[0.4220, -0.4401, -0.1647, 0.0001], [0.2378, -0.4904, 0.0205, 0.3069], [-0.4410, -0.3263, -0.3824, -0.1055], [0.2296, -0.4337, 0.0585, -0.4768]])
# A3 = np.array([[-0.1583, 0.0180, -0.0976, 0.2688], [-0.2910, -0.3531, -0.1873, 0.0120], [-0.0247, 0.4154, 0.2695, -0.2676], [-0.1972, 0.0089, 0.0032, 0.2430]])
# A4 = np.array([[-0.9491, -0.1419, -0.3721, 0.2278], [0.4074, -0.4881, 0.9128, 0.3070], [-0.0201, -0.2605, 0.5302, -0.9388], [-0.5581, -0.4818, -0.3143, 0.4272]])
#
# print("If A1 is stable: ", check_stable(A1))
# print("If A2 is stable: ", check_stable(A2))
# print("If A3 is stable: ", check_stable(A3))
# print("If A4 is stable: ", check_stable(A4))


# Problem 2 - Controllability
# check this mat is full row rank [A^(n-1)B A^(n-2)B ... AB B]
def check_controllable(A, B):
    num_of_input = A.shape[0]

    mat_need_check = B

    for i in range(1, num_of_input):
        mat_need_check = np.concatenate((np.matmul(A, B), mat_need_check), axis=1)
        A = np.matmul(A, A)

    return np.linalg.matrix_rank(mat_need_check) == num_of_input


# A1 = np.array([[0.0000, 1.0000, -1.5000, -1.5000], [-2.0000, 0.5000, 1.0000, 0.0000], [0.0000, 0.0000, 0.0000, 0.0000], [-0.5000, 1.5000, 0.0000, 0.0000]])
# A2 = np.array([[0.0000, -0.5000, -0.5000, 0.0000], [0.0000, -1.0000, 0.0000, 0.0000], [0.0000, 0.5000, 0.0000, -0.5000], [-1.5000, 0.0000, -1.5000, 0.0000]])
# A3 = np.array([[0.5000, 0.0000, 0.0000, 0.0000], [0.0000, 0.0000, 0.0000, 1.5000], [0.0000, 2.0000, 0.5000, -0.5000], [0.0000, 0.0000, -0.5000, 0.0000]])
# A4 = np.array([[0.0000, -1.5000, -1.5000, 1.0000], [-2.0000, 0.0000, 0.0000, 1.5000], [0.0000, 0.0000, 0.0000, 0.0000], [0.0000, 0.0000, 0.0000, 0.0000]])
# B1 = np.array([[-0.5000, 0.0000], [0.0000, 0.5000], [0.0000, 0.0000], [0.0000, 0.0000]])
# B2 = np.array([[0.0000, 0.0000, 0.0000], [0.0000, -1.0000, 0.0000], [-0.5000, 0.0000, 0.5000], [0.0000, 0.0000, 0.0000]])
# B3 = np.array([[0.5000, -1.0000], [0.0000, 0.0000], [0.0000, 0.0000], [0.0000, 0.0000]])
# B4 = np.array([[0.5000], [0.0000], [0.0000], [0.0000]])
#
# print("Check A1, B1 is controllable: ", check_controllable(A1, B1))
# print("Check A2, B2 is controllable: ", check_controllable(A2, B2))
# print("Check A3, B3 is controllable: ", check_controllable(A3, B3))
# print("Check A4, B4 is controllable: ", check_controllable(A4, B4))


# Problem 3, solve LQR by iterating the Riccati equations
def solve_LQR(A, B, Q, R, QN, N):
    list_of_P = []
    list_of_K = []

    list_of_P.append(QN)

    for i in range(N):
        K_i = -1 * np.linalg.inv(B.transpose().dot(list_of_P[i]).dot(B) + R).dot(B.transpose()).dot(list_of_P[i]).dot(A)
        P_i = Q + A.transpose().dot(list_of_P[i]).dot(A) + A.transpose().dot(list_of_P[i]).dot(B).dot(K_i)
        list_of_K.append(K_i)
        list_of_P.append(P_i)

    return list_of_P[::-1], list_of_K[::-1]


# Problem 4, calc the control unit and the states based on Problem 3
def calc_control_unit_states_LQR(A, B, Q, R, QN, N, x0):
    P_mats, K_mats = solve_LQR(A, B, Q, R, QN, N)

    nc = B.shape[1]
    ns = A.shape[0]

    state_mat = np.zeros((ns, N + 1))
    control_unit_mat = np.zeros((nc, N))
    list_of_costs = []

    state_mat[:, 0] = x0[:, 0]

    for i in range(N):
        # calculate the next state
        current_state_x = state_mat[:, i]
        control_unit = K_mats[i].dot(current_state_x)
        next_state_x = A.dot(current_state_x) + B.dot(control_unit)
        # print("Next State is: ", next_state_x)
        state_mat[:, i + 1] = next_state_x
        control_unit_mat[:, i] = control_unit

        # calculate the cost
        current_cost = current_state_x.transpose().dot(P_mats[i]).dot(current_state_x)
        list_of_costs.append(current_cost)

    optimal_cost = list_of_costs[0]
    return state_mat, control_unit_mat, optimal_cost


# A = np.array([[0., 0., 0.],
#               [0., 2., -1.],
#               [-0.5, 0., 0.]])
# B = np.array([[0.5, 1.],
#               [0., 0.],
#               [0., 0.]])
# N = 17
#
# Q = np.array([[0.39950948, 0., 0.],
#               [0., 0.34586236, 0.],
#               [0., 0., 0.93609158]])
# R = np.array([[68.40384321, 0.],
#               [0., 59.66342226]])
#
# QN = np.array([[1309.52285892, 0., 0.],
#                [0., 1472.42957394, 0.],
#                [0., 0., 1467.15140134]])
# x0 = np.array([[1.74797056],
#                [-5.45509213],
#                [-13.57720187]])
#
# x_optimal, u_optimal, J_optimal = calc_control_unit_states_LQR(A, B, Q, R, QN, N, x0)


# Problem 5
# First solve the riccati equation, then check for cost_to_go
import scipy.linalg


def check_if_QR_correct(A, B, Q, R, x0, J0):
    P_mat = scipy.linalg.solve_discrete_are(A, B, Q, R)
    # print("P_mat is: ", P_mat)
    K_mat = -1 * np.linalg.inv(B.transpose().dot(P_mat).dot(B) + R).dot(B.transpose()).dot(P_mat).dot(A)
    print("K_mat is: ", K_mat)

    cost_to_go = x0.transpose().dot(P_mat).dot(x0)
    print("cost_to_go is: ", cost_to_go)
    eps = 1e-3
    return K_mat, np.abs(cost_to_go - J0) < eps


J0 = 9006.60795076842
x0 = np.array([[11.00048327], [6.94634683], [0.81084986], [19.66547799], [19.98144722]])
A = np.array([[-2.00000000, 0.00000000, 0.00000000, 0.00000000, -0.50000000], [0.00000000, 0.00000000, 0.00000000, 0.00000000, -0.50000000], [0.00000000, -1.50000000, 0.00000000, 0.00000000, 0.00000000], [-0.50000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000], [0.50000000, 2.00000000, -1.50000000, 0.00000000, 0.00000000]])
B = np.array([[-1.00000000, 0.00000000, 0.00000000], [0.00000000, 0.00000000, 0.50000000], [0.00000000, 0.00000000, 0.00000000], [0.00000000, -0.50000000, 0.00000000], [0.00000000, 0.00000000, 0.00000000]])
Q1 = np.array([[4.75553661, 0.23594742, -1.85188635, 0.09686498, 0.77559168], [0.23594742, 4.03347436, 1.22250517, -0.24010438, -0.18205893], [-1.85188635, 1.22250517, 3.13419454, 0.00691619, 2.17553471], [0.09686498, -0.24010438, 0.00691619, 4.17274607, -0.37899509], [0.77559168, -0.18205893, 2.17553471, -0.37899509, 3.85632512]])
R1 = np.array([[2.43632992, 0.67375308, -0.60103291], [0.67375308, 5.17862235, -0.65577883], [-0.60103291, -0.65577883, 1.23552297]])
Q2 = np.array([[7.50032336, 0.00205943, 0.74374363, -0.17907344, -0.96671159], [0.00205943, 6.72214628, -2.25882231, 0.27754093, 0.57807914], [0.74374363, -2.25882231, 4.21183739, 1.06501520, 1.46093916], [-0.17907344, 0.27754093, 1.06501520, 7.05311083, 0.22633175], [-0.96671159, 0.57807914, 1.46093916, 0.22633175, 7.52617484]])
R2 = np.array([[3.13064463, 0.46045723, 2.61986340], [0.46045723, 5.39580443, 1.90788213], [2.61986340, 1.90788213, 6.16606176]])
Q3 = np.array([[5.25704515, 0.75298572, -1.49685678, 2.04524029, 1.02152638], [0.75298572, 4.31348750, -0.43971694, 0.89431956, 0.27574644], [-1.49685678, -0.43971694, 6.45128492, 0.34887088, -1.41383467], [2.04524029, 0.89431956, 0.34887088, 7.32410039, -0.30876351], [1.02152638, 0.27574644, -1.41383467, -0.30876351, 3.97843553]])
R3 = np.array([[3.50569814, -0.96481618, -0.87910807], [-0.96481618, 3.01376960, -1.51252763], [-0.87910807, -1.51252763, 5.02925247]])
Q4 = np.array([[7.11842471, 0.84103411, 0.37602320, 0.81823852, 1.49155207], [0.84103411, 3.16832395, 2.18953445, -0.08031540, 0.77023228], [0.37602320, 2.18953445, 4.64487718, 1.16735072, -1.90299955], [0.81823852, -0.08031540, 1.16735072, 3.06250201, -0.57438049], [1.49155207, 0.77023228, -1.90299955, -0.57438049, 2.64653429]])
R4 = np.array([[1.01351050, 1.11593390, -0.61117503], [1.11593390, 5.66894661, -0.69130435], [-0.61117503, -0.69130435, 1.78002370]])

test_kmat, check_result = check_if_QR_correct(A, B, Q1, R1, x0, J0)
test_kmat, check_result = check_if_QR_correct(A, B, Q2, R2, x0, J0)
test_kmat, check_result = check_if_QR_correct(A, B, Q3, R3, x0, J0)
test_kmat, check_result = check_if_QR_correct(A, B, Q4, R4, x0, J0)


test_P, test_K = solve_LQR(A, B, Q4, R4, Q4, 500)
test_state, test_control, test_cost = calc_control_unit_states_LQR(A, B, Q4, R4, Q4, 500, x0)
