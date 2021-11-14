import numpy
import numpy as np


def get_rotation_matrix(theta):
    rotation = np.matrix([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return rotation


def check_if_rotation_matrix(mat):
    eps = 1e-7
    identity_mat = np.matrix(np.identity(mat.shape[0]))
    result = False
    if (np.abs(np.matmul(mat, mat.T) - identity_mat) < eps).all() and (np.abs(np.matmul(mat.T, mat) - identity_mat) <
                                                                        eps).all() \
            and np.abs(np.linalg.det(mat) - 1) < eps:
        result = True

    return result


def get_rotation_and_translation_from_transform_matrix(transformation):
    rotation = transformation[0: 3, 0: 3]

    translation = transformation[0:3, 3]
    translation = np.resize(translation, (3, 1))

    return [rotation, translation]


def get_transformation_matrix_from_rotation_and_translation(rotation, translation):
    const_vec = np.array([[0, 0, 0, 1]])
    return np.append(np.append(rotation, translation, axis=1), const_vec, axis=0)


def get_inverse_of_transformation(transformation):
    [rotation, translation] = get_rotation_and_translation_from_transform_matrix(transformation)
    rotation = rotation.transpose()

    const = np.array([[0, 0, 0, 1]])

    result = np.append(rotation, np.matmul(-rotation, translation), axis=1)
    result = np.append(result, const, axis=0)
    return result


def get_rotation_matrix_of_axis(theta, axis_type):  # 0, 1, 2 for x, y, z
    if axis_type == 0:
        result = np.array(
            [[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    elif axis_type == 1:
        result = np.array(
            [[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    else:
        result = np.array(
            [[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return result


def get_skew_symmetric_mat(vec):
    result = np.array([[0, -vec[2, 0], vec[1, 0]], [vec[2, 0], 0, -vec[0, 0]], [-vec[1, 0], vec[0, 0], 0]])
    return result


def get_vector_from_skew_symmetric(mat):
    result = np.array([[mat[2, 1]], [mat[0, 2]], [mat[1, 0]]])
    return result


def rodrigues_form(rot_axis, theta):
    bracket_operator = get_skew_symmetric_mat(rot_axis)
    return np.identity(3) + np.sin(theta) * bracket_operator + (1 - np.cos(theta)) * np.matmul(bracket_operator, bracket_operator)


def log_of_rotation_matrix(rotation_mat):
    theta = np.arccos((np.matrix.trace(rotation_mat) - 1) / 2)
    axis = get_vector_from_skew_symmetric((rotation_mat - rotation_mat.T) / (2 * np.sin(theta)))
    return [axis, theta]


def get_angular_velocity_and_linear_velocity_from_twist_vector(twist_vector):
    angular_velocity = twist_vector[0: 3]
    linear_velocity = twist_vector[3: 6]

    angular_velocity = np.resize(angular_velocity, (3, 1))
    linear_velocity = np.resize(linear_velocity, (3, 1))
    return [angular_velocity, linear_velocity]


def get_bracket_of_twist_vector(twist_vector):
    [angular_w, linear_v] = get_angular_velocity_and_linear_velocity_from_twist_vector(twist_vector)
    bracket_w = get_skew_symmetric_mat(angular_w)

    result = np.append(bracket_w, linear_v, axis=1)
    const = np.array([[0, 0, 0, 0]])
    result = np.append(result, const, axis=0)

    return result


def get_twist_vector_from_bracket(twist_bracket):
    linear_velocity = twist_bracket[0:3, 3]
    linear_velocity = np.resize(linear_velocity, (3, 1))
    angular_velocity = np.array([[twist_bracket[2, 1]], [twist_bracket[0, 2]], [twist_bracket[1, 0]]])

    result = np.append(angular_velocity, linear_velocity, axis=0)
    return result


def get_adjoint_representation_of_transformation(transformation):
    [rotation, translation] = get_rotation_and_translation_from_transform_matrix(transformation)
    zero_mat = np.zeros((3, 3))

    adjoint_mat = np.append(np.append(rotation, zero_mat, axis=1),
                            np.append(numpy.matmul(get_skew_symmetric_mat(translation), rotation), rotation, axis=1), axis=0)
    return adjoint_mat


# V = np.array([[10], [-7], [ 5], [-9], [-5], [6]])
# hw4_2_result = get_bracket_of_twist_vector(V)
#
# T = np.array([[0.03004919, -0.99753073, -0.06347830, -0.85964130], [-0.81868120, -0.06099740, 0.57099948, 0.70635388], [-0.57346154, 0.03481042, -0.81849258, -0.42285615], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
# hw4_6_result = get_adjoint_representation_of_transformation(T)
#
# V_sb_in_b = np.array([[0.54444771], [-0.98736870], [-0.75803998], [-0.16655871], [0.54692846], [-0.16952801]])
# T_sb = np.array([[0.42695810, -0.66750826, 0.61003238, -0.46099771], [0.75472973, 0.63463481, 0.16619775, -0.72440365], [-0.49808615, 0.38945010, 0.77475081, -0.84353823], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
#
# hw4_7_result = np.matmul(get_adjoint_representation_of_transformation(T_sb), V_sb_in_b)


def exp_of_twist_vector(twist_vector):
    [angular_w, linear_v] = get_angular_velocity_and_linear_velocity_from_twist_vector(twist_vector)
    zero_vec = np.array([[0], [0], [0]])
    const_vec = np.array([[0, 0, 0, 1]])
    if np.array_equal(zero_vec, angular_w):
        result = np.append(np.append(np.identity(3), linear_v, axis=1), const_vec, axis=0)
    else:
        rotation_theta = np.linalg.norm(angular_w)
        rotation_axis = angular_w / rotation_theta

        rotation_part = rodrigues_form(rotation_axis, rotation_theta)
        bracket_w = get_skew_symmetric_mat(rotation_axis)
        J_mat = np.identity(3) + 1 / rotation_theta * ((1 - np.cos(rotation_theta)) * bracket_w
                                                       + (rotation_theta - np.sin(rotation_theta)) * np.matmul(bracket_w, bracket_w))

        translation_part = np.matmul(J_mat, linear_v)
        result = np.append(np.append(rotation_part, translation_part, axis=1), const_vec, axis=0)

    return result


# M = np.array([[-0.28876404, -0.36858617, -0.88360600, -1.58836284], [-0.91622800, -0.16135211, 0.36673117, 0.42132854], [-0.27774373, 0.91548333, -0.29111628, 0.05230257], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
# V_b = np.array([[0.90705942], [0.55415244], [0.31002948], [-0.96980220], [-0.97244608], [0.23375108]])
# V_s = np.matmul(get_adjoint_representation_of_transformation(M), V_b)
# hw4_3_result = np.matmul(exp_of_twist_vector(V_s), M)


def log_of_twist_matrix(twist_matrix):
    [rotation_mat, translation] = get_rotation_and_translation_from_transform_matrix(twist_matrix)

    if (rotation_mat == np.identity(3)).all():
        return np.append(np.array([[0], [0], [0]]), translation, axis=0)
    else:
        [rotation_axis, rotation_angle] = log_of_rotation_matrix(rotation_mat)
        angular_velocity = rotation_angle * rotation_axis

        bracket_w = get_skew_symmetric_mat(rotation_axis)
        # bracket_w = get_skew_symmetric_mat(rotation_angle * rotation_axis)
        A_inverse_mat = (1 / rotation_angle) * np.identity(3) - \
                        (0.5 * bracket_w) + \
                        (1 / rotation_angle - 0.5 / np.tan(rotation_angle / 2)) * np.matmul(bracket_w, bracket_w)

        linear_velocity = rotation_angle * np.matmul(A_inverse_mat, translation)
        # linear_velocity = np.matmul(A_inverse_mat, translation)
    return np.append(angular_velocity, linear_velocity, axis=0)


# T_1in0 = np.array([[0.83825062, -0.04571062, -0.54336584, 0.44670818], [0.44617915, 0.63033825, 0.63529352, -0.34643369], [0.31346461, -0.77497369, 0.54877656, 1.01477179], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
# hw4_4_result = log_of_twist_matrix(T_1in0)
#
# T_sb = np.array([[-0.81182787, -0.23909123, -0.53270151, 0.88023830], [-0.38310045, -0.47039111, 0.79496305, 0.84636676], [-0.44064675, 0.84945134, 0.29028065, -0.99794904], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
# V_sb_in_s = np.array([[-0.77474997], [-0.46625816], [0.63649500], [0.31720528], [1.58147805], [0.03295729]])
# q_B = np.array([[-0.99462671], [-1.77815213], [-0.35471397], [1.00000000]])
# q_S = np.matmul(T_sb, q_B)
# hw4_8_result = np.matmul(get_bracket_of_twist_vector(V_sb_in_s), q_S)
# V_inb = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(T_sb)), V_sb_in_s)
# hw4_8_result = np.matmul(get_bracket_of_twist_vector(V_inb), q_B)

t = 2.92185510
T_1in0 = np.array([[0.29168105, 0.81610731, 0.49888979, 0.86272871], [0.89158226, -0.04307703, -0.45080533, 0.41182782], [-0.34641484, 0.57629266, -0.74019155, -0.13041287], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
p_2in0 = np.array([-0.11837483, -1.36839026, -0.20222991])
R_2in0 = np.array([[-0.19154060, -0.23650310, 0.95256416], [0.27421688, -0.94478015, -0.17943124], [0.94239976, 0.22684080, 0.24581690]])
p_2in0 = np.resize(p_2in0, (3, 1))
T_2in0 = np.append(np.append(R_2in0, p_2in0, axis=1), np.array([[0, 0, 0, 1]]), axis=0)
T_12 = np.matmul(get_inverse_of_transformation(T_1in0), T_2in0)
hw4_5_result = log_of_twist_matrix(T_12) / t

# HW 5
# problem 1
# T_01_0 = np.array([[-1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 4], [0, 0, 0, 1]])
# rot_theta = -0.51

# rot_mat = get_rotation_matrix_of_axis(rot_theta, 0)
# translation = [[0], [0], [0]]
# transformation_mat = get_transformation_matrix_from_rotation_and_translation(rot_mat, translation)
# twist_vec = np.array([[-1], [0], [0], [0], [-2], [0]])
# twist_vec = twist_vec * rot_theta

# hw5_1_result = np.matmul(T_01_0, transformation_mat)
# hw5_1_result = np.matmul(exp_of_twist_vector(twist_vec), T_01_0)


# problem 4
# T_01_0 = np.array([[-1, 0, 0, -4], [0, 0, 1, 0], [0, 1, 0, 6], [0, 0, 0, 1]])
# twist_1 = np.array([[0], [-1], [0], [2], [0], [2]])
# twist_2 = np.array([[0], [0], [0], [0], [-1], [0]])
# twist_3 = np.array([[0], [0], [0], [0], [0], [1]])
# thetas = np.array([[-0.13, 0.06, -0.12]])
#
# hw5_4_result = np.matmul(exp_of_twist_vector(twist_3 * thetas[0, 2]), T_01_0)
# hw5_4_result = np.matmul(exp_of_twist_vector(twist_2 * thetas[0, 1]), hw5_4_result)
# hw5_4_result = np.matmul(exp_of_twist_vector(twist_1 * thetas[0, 0]), hw5_4_result)

# Input the spatial screw axis
Spatial_Screw_Axises = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, -1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1],
                                 [0, -0.36, 0, 0.78, 0, -1.18, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
# get the initial end-effector pose
T_base_to_endeffector = get_transformation_matrix_from_rotation_and_translation(np.identity(3), np.array([[0], [0], [1.301]]))


theta = np.array([-1.2, 0.7, 2.8, 0.7, 1.2, 0.2, 0.3])
# theta = np.array([0.2, -0.2, 0.5, -0.4, 1.2, -0.8, 0.4])
# theta = np.array([0, 0, 0, 0, 0, 0, 0])
# Forward Kinematics Part
for i in range(0, 7):
    spatial_screw_axis = Spatial_Screw_Axises[:, [7 - i - 1]]
    T_base_to_endeffector = np.matmul(exp_of_twist_vector(spatial_screw_axis * theta[7 - i - 1]), T_base_to_endeffector)

Spatial_Jacobian = np.array([[], [], [], [], [], []])
multi_mat = np.identity(4)

sca = Spatial_Screw_Axises[:, 0].reshape(6, 1)

# Compute Spatial Jacobian
for i in range(0, 7):
    spatial_screw_axis = Spatial_Screw_Axises[:, [i]]
    Jacobian_i = np.matmul(get_adjoint_representation_of_transformation(multi_mat), spatial_screw_axis)

    Spatial_Jacobian = np.append(Spatial_Jacobian, Jacobian_i, axis=1)

    if i != 6:
        multi_mat = np.matmul(multi_mat, exp_of_twist_vector(spatial_screw_axis * theta[i]))
