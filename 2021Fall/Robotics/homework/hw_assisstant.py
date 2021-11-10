import numpy
import numpy as np

eps = 1e-5


def get_rotation_matrix(theta):
    rotation = np.matrix([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return rotation


def check_if_rotation_matrix(mat):
    identity_mat = np.matrix(np.identity(mat.shape[0]))
    result = False
    if (np.abs(mat * mat.T - identity_mat) < eps).all() and (np.abs(mat.T * mat - identity_mat) < eps).all() \
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


V = np.array([[10], [-7], [ 5], [-9], [-5], [6]])
hw4_2_result = get_bracket_of_twist_vector(V)

T = np.array([[0.03004919, -0.99753073, -0.06347830, -0.85964130], [-0.81868120, -0.06099740, 0.57099948, 0.70635388], [-0.57346154, 0.03481042, -0.81849258, -0.42285615], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
hw4_6_result = get_adjoint_representation_of_transformation(T)

V_sb_in_b = np.array([[0.54444771], [-0.98736870], [-0.75803998], [-0.16655871], [0.54692846], [-0.16952801]])
T_sb = np.array([[0.42695810, -0.66750826, 0.61003238, -0.46099771], [0.75472973, 0.63463481, 0.16619775, -0.72440365], [-0.49808615, 0.38945010, 0.77475081, -0.84353823], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])

hw4_7_result = np.matmul(get_adjoint_representation_of_transformation(T_sb), V_sb_in_b)


def exp_of_twist_vector(twist_vector):
    [angular_w, linear_v] = get_angular_velocity_and_linear_velocity_from_twist_vector(twist_vector)
    zero_vec = np.array([[0], [0], [0]])
    const_vec = np.array([[0, 0, 0, 1]])
    if (zero_vec == angular_w).all():
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


M = np.array([[-0.28876404, -0.36858617, -0.88360600, -1.58836284], [-0.91622800, -0.16135211, 0.36673117, 0.42132854], [-0.27774373, 0.91548333, -0.29111628, 0.05230257], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
V_b = np.array([[0.90705942], [0.55415244], [0.31002948], [-0.96980220], [-0.97244608], [0.23375108]])
V_s = np.matmul(get_adjoint_representation_of_transformation(M), V_b)
hw4_3_result = np.matmul(exp_of_twist_vector(V_s), M)


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


T_1in0 = np.array([[0.83825062, -0.04571062, -0.54336584, 0.44670818], [0.44617915, 0.63033825, 0.63529352, -0.34643369], [0.31346461, -0.77497369, 0.54877656, 1.01477179], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
hw4_4_result = log_of_twist_matrix(T_1in0)

T_sb = np.array([[-0.81182787, -0.23909123, -0.53270151, 0.88023830], [-0.38310045, -0.47039111, 0.79496305, 0.84636676], [-0.44064675, 0.84945134, 0.29028065, -0.99794904], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
V_sb_in_s = np.array([[-0.77474997], [-0.46625816], [0.63649500], [0.31720528], [1.58147805], [0.03295729]])
q_B = np.array([[-0.99462671], [-1.77815213], [-0.35471397], [1.00000000]])
# q_S = np.matmul(T_sb, q_B)
# hw4_8_result = np.matmul(get_bracket_of_twist_vector(V_sb_in_s), q_S)
V_inb = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(T_sb)), V_sb_in_s)
hw4_8_result = np.matmul(get_bracket_of_twist_vector(V_inb), q_B)

t = 1.13289126
T_1in0 = np.array([[-0.03490204, -0.28636706, 0.95748407, -0.25986619], [-0.99562334, 0.09307340, -0.00845563, -0.85298021], [-0.08669488, -0.95358862, -0.28836219, -0.84704426], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
p_2in0 = np.array([-1.09934784, 0.08752813, -1.50066555])
R_2in0 = np.array([[0.81711787, 0.06079288, 0.57325614], [-0.11881654, 0.99083305, 0.06428457], [-0.56409309, -0.12064038, 0.81685059]])
p_2in0 = np.resize(p_2in0, (3, 1))
T_2in0 = np.append(np.append(R_2in0, p_2in0, axis=1), np.array([[0, 0, 0, 1]]), axis=0)
T_12 = np.matmul(get_inverse_of_transformation(T_1in0), T_2in0)
hw4_5_result = log_of_twist_matrix(T_12) / t

# HW 5
# problem 1
T_01_0 = np.array([[-1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 4], [0, 0, 0, 1]])
rot_theta = -0.51

# rot_mat = get_rotation_matrix_of_axis(rot_theta, 0)
# translation = [[0], [0], [0]]
# transformation_mat = get_transformation_matrix_from_rotation_and_translation(rot_mat, translation)
twist_vec = np.array([[-1], [0], [0], [0], [-2], [0]])
twist_vec = twist_vec * rot_theta

# hw5_1_result = np.matmul(T_01_0, transformation_mat)
hw5_1_result = np.matmul(exp_of_twist_vector(twist_vec), T_01_0)


# problem 4
T_01_0 = np.array([[0, 1, 0, -2], [-1, 0, 0, 0], [0, 0, 1, -4], [0, 0, 0, 1]])
twist_1 = np.array([[-1], [0], [0], [0], [0], [0]])
twist_2 = np.array([[0], [-1], [0], [0], [0], [4]])
twist_3 = np.array([[0], [-1], [0], [2], [0], [2]])
thetas = np.array([[-0.26000000, 0.24000000, 0.62000000]])

hw5_4_result = np.matmul(exp_of_twist_vector(twist_3 * thetas[0, 2]), T_01_0)
hw5_4_result = np.matmul(exp_of_twist_vector(twist_2 * thetas[0, 1]), hw5_4_result)
hw5_4_result = np.matmul(exp_of_twist_vector(twist_1 * thetas[0, 0]), hw5_4_result)

T_2_in_0 = np.array([[-0.39161000, -0.81674292, -0.42376008, 0.36056999], [-0.10549836, -0.41765068, 0.90246219, 0.13076578], [-0.91406329, 0.39811922, 0.07739114, 0.12649139], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])

T12 = np.matmul(get_inverse_of_transformation(hw5_4_result), T_2_in_0)

[rot1, trans1] = get_rotation_and_translation_from_transform_matrix(hw5_4_result)
[rot2, trans2] = get_rotation_and_translation_from_transform_matrix(T_2_in_0)
distance = np.linalg.norm(trans1 - trans2)

# HW 6
# Problem 2
dtheta = -0.39
screw_axis = np.array([[0], [0], [0], [0], [1], [0]])
hw6_2_result = screw_axis * dtheta
T_sb = np.array([[-1, 0, 0, -2], [0, 0, 1, 0], [0, 1, 0, -2], [0, 0, 0, 1]])
hw6_2_result = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(T_sb)), hw6_2_result)

# Problem 3
theta = np.array([[0.11000000], [0.64000000], [-0.53000000], [-0.79000000], [-0.11000000], [-0.45000000], [0.23000000], [0.03000000], [0.08000000]])
dtheta = np.array([[-0.52000000], [0.40000000], [0.57000000], [-0.84000000], [0.13000000], [-0.16000000], [0.81000000], [-0.63000000], [0.26000000]])
jacobian = np.array([[0.00000000, -0.02692881, -0.97685182, 0.00000000, -0.13051632,  0.95234177, 0.00239708, 0.99680171, -0.00000000], [0.00000000, 0.12013991, 0.20759098, 0.00000000, -0.38711935,  -0.30495638, 0.02989957, -0.07991469, -0.00000000], [0.00000000, 0.99239168, -0.05163830, 0.00000000, 0.91274537, 0.00683830,  0.99955003, -0.00000000, 1.00000000], [-0.75358851, -0.43184181, -0.48964581, -0.13051632, -1.15917798,  -0.00896494, -3.98630977, -0.00000000, 0.00000000], [-0.65471033, 3.34636289, -2.51687613, -0.38711935, 3.23972567,  0.07299397, 2.31868693, -0.00000000, 2.00000000], [0.05881105, -0.41683211, -0.85536088, 0.91274537, 1.20829848,  4.50370211, -0.05979913, 2.15982939, 0.00000000]])
T_1in0 = np.array([[0.65679464, -0.74627125, 0.10816663, 3.88998167], [-0.75358851, -0.65471033, 0.05881105, -0.71601314], [0.02692881, -0.12013991, -0.99239168, 2.45171674], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
hw6_3_result = np.matmul(get_adjoint_representation_of_transformation(T_1in0), np.matmul(jacobian, dtheta))

# Problem 4
theta = np.array([[-0.26000000], [0.24000000], [0.62000000]])
dtheta = np.array([[0.12795753], [0.45883433], [0.15448126]])
spatial_screw_axis = np.array([[-1, 0, 0], [0, 0, 0], [0, 0, 0], [0, -1, 0], [0, 0, -1], [0, 0, 0]])
multi_mat = np.identity(4)
Spatial_Jacobian = np.array([[], [], [], [], [], []])

for i in range(0, 3):
    screw_axis = spatial_screw_axis[:, i]
    screw_axis = np.resize(screw_axis, (6, 1))

    Jacobian_i = np.matmul(get_adjoint_representation_of_transformation(multi_mat), screw_axis)

    Spatial_Jacobian = np.append(Spatial_Jacobian, Jacobian_i, axis=1)
    if i != 2:
        multi_mat = np.matmul(multi_mat, exp_of_twist_vector(screw_axis * theta[i]))


body_screw_axis = np.array([[0, 0, 0], [-1, 0, 0], [0, 0, 0], [4, 0, 1], [0, -1, 0], [0, 0, 0]])
body_screw_axis_2 = np.resize(body_screw_axis[:, 2], (6, 1))
body_screw_axis_1 = np.resize(body_screw_axis[:, 1], (6, 1))
body_screw_axis_0 = np.resize(body_screw_axis[:, 0], (6, 1))

Body_Jacobian_2 = body_screw_axis_2
Body_Jacobian_1 = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(exp_of_twist_vector(body_screw_axis_2 * theta[2]))), body_screw_axis_1)
tmpMat = np.matmul(get_inverse_of_transformation(exp_of_twist_vector(body_screw_axis_2 * theta[2])), get_inverse_of_transformation(exp_of_twist_vector(body_screw_axis_1 * theta[1])))
Body_Jacobian_0 = np.matmul(get_adjoint_representation_of_transformation(tmpMat), body_screw_axis_0)
Body_Jacobian = np.append(Body_Jacobian_0, np.append(Body_Jacobian_1, Body_Jacobian_2, axis=1), axis=1)

# Waste

# R_0 = np.array([[-0.09357520, 0.99285489, -0.07404627], [-0.37694995, -0.10416650, -0.92035758], [-0.92149466, -0.05821090, 0.38400401]])
# R_1 = np.array([[-0.09357520, -0.37694995, -0.92149466], [0.99285489, -0.10416650, -0.05821090], [-0.07404627, -0.92035758, 0.38400401]])
# R_2 = np.array([[-0.34421484, -0.42542507, 0.52851159], [0.13978150, -0.04668462, -0.46924688], [0.94733750, -0.13341728, 0.80009817]])
# R_3 = np.array([[0.56064421, 0.52738543, -0.27336646], [-0.73235060, -0.61820324, 0.83480724], [0.72441223, -0.25041119, 0.43096606]])
#
# M = np.array([[0.19860057, 0.86927278, -0.45268383, -2.01604063], [-0.62982488, 0.46708315, 0.62060773, -1.66702011], [0.75091839, 0.16185849, 0.64025260, -0.19014183], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
# V_s = np.array([[-0.61399203], [-0.46576343], [-0.76459553], [-0.19144771], [0.03994459], [0.53406147]])
# test_result = np.matmul(exp_of_twist_vector(V_s), M)

# midterm 1.8 answer is
#
# 1.     [[-1.        ,  0.        ,  0.        ],
#        [ 0.        ,  0.        ,  0.        ],
#        [ 0.        ,  0.        ,  0.        ],
#        [ 0.        , -1.        ,  0.        ],
#        [ 0.        ,  0.        , -0.96638998],
#        [ 0.        ,  0.        , -0.25708055]]
#
# 2.     [[ 0.  ,  0.  ,  0.  ],
#        [-1.  ,  0.  ,  0.  ],
#        [ 0.  ,  0.  ,  0.  ],
#        [ 4.  ,  0.  ,  1.  ],
#        [ 0.  , -1.  ,  0.  ],
#        [ 0.62,  0.  ,  0.  ]]
#
# 3.     [[-0.12795753],
#        [ 0.        ],
#        [ 0.        ],
#        [-0.45883433],
#        [-0.14928914],
#        [-0.03971413]]
#
# 4.     [[ 0.34597528],
#        [-0.29936071],
#        [ 0.34772418]]
