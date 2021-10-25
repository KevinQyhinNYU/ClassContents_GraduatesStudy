import numpy

eps = 1e-7


def get_rotation_matrix(theta):
    rotation = numpy.matrix([[numpy.cos(theta), -numpy.sin(theta)], [numpy.sin(theta), numpy.cos(theta)]])
    return rotation


def check_if_rotation_matrix(mat):
    identity_mat = numpy.matrix(numpy.identity(mat.shape[0]))
    result = False
    if (numpy.abs(mat * mat.T - identity_mat) < eps).all() and (numpy.abs(mat.T * mat - identity_mat) < eps).all() \
            and numpy.abs(numpy.linalg.det(mat) - 1) < eps:
        result = True

    return result


R1 = numpy.matrix([[0.76852530, 0.14901919, -0.34157729], [-0.28941616, 0.85881182, 0.10018243],
                   [0.26190624, -0.07990144, 0.69005302]])
R2 = numpy.matrix([[-0.50849128, 0.83494196, -0.21049592], [0.18924893, 0.34684950, 0.91862956],
                   [0.84001277, 0.42727899, -0.33438182]])
R3 = numpy.matrix([[-0.59991548, 0.15483486, 0.78493795], [-0.70273769, -0.57095371, -0.42446626],
                   [0.38244106, -0.80624936, 0.45133226]])
R4 = numpy.matrix([[-0.87497713, -0.47070661, -0.11335921], [0.43575148, -0.66354445, -0.60813601],
                   [0.21103477, -0.58150154, 0.78569732]])
R5 = numpy.matrix([[-0.14091741, -0.84568600, -0.66265077], [-0.23418136, 0.74713955, -0.64246995],
                   [0.95853887, 0.13011092, -0.28765377]])

print("Is {} a rotation matrix: \n".format("R1"), check_if_rotation_matrix(R1))
print("Is {} a rotation matrix: \n".format("R2"), check_if_rotation_matrix(R2))
print("Is {} a rotation matrix: \n".format("R3"), check_if_rotation_matrix(R3))
print("Is {} a rotation matrix: \n".format("R4"), check_if_rotation_matrix(R4))
print("Is {} a rotation matrix: \n".format("R5"), check_if_rotation_matrix(R5))

p_0 = numpy.array([[0.10722973], [-0.58334760]])
R_40 = numpy.array([[-0.50656629, 0.86220102], [-0.86220102, -0.50656629]])
q_0 = numpy.array([[0.73868153], [0.24810498]])
q_4 = numpy.matmul(R_40, q_0) + p_0
print("q_4 is : \n", q_4)
print("\n")

T_04 = numpy.array(
    [[0.93206637, 0.27038449, -0.24113171, -0.82928384], [0.16835921, 0.26608178, 0.94913416, 0.45283116],
     [0.32079191, -0.92525278, 0.20248416, -0.56450363], [0.000000, 0.00000000, 0.00000000, 1.00000000]])
p_4 = numpy.array([[0], [1], [1], [1]])
p_0 = numpy.matmul(T_04, p_4)
print("p_0 is : \n", p_0)
print("\n")

M = numpy.matrix([[2], [2]])
print(get_rotation_matrix(numpy.pi / 6.0) * M)


def get_inverse_of_transformation(transformation):
    rotation = transformation[0: 3, 0: 3]
    rotation = rotation.transpose()

    translation = transformation[0:3, 3]
    translation = numpy.resize(translation, (3, 1))

    const = numpy.array([[0, 0, 0, 1]])

    result = numpy.append(rotation, numpy.matmul(-rotation, translation), axis=1)
    result = numpy.append(result, const, axis=0)
    return result


T_8in0 = numpy.array(
    [[0.42734620, -0.52768407, 0.73411494, -0.15899131], [-0.90189692, -0.30532058, 0.30555081, 0.24010015],
     [0.06290610, -0.79267198, -0.60639423, 0.90700601], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
T_6in8 = numpy.array(
    [[-0.77961294, -0.57815721, -0.24070293, -0.14187170], [0.00816554, 0.37493194, -0.92701638, -0.10927903],
     [0.62620842, -0.72467944, -0.28758083, -0.54832063], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])

pose_6in0 = numpy.matmul(T_8in0, T_6in8)


def get_rotation_matrix_of_axis(theta, axis_type):  # 0, 1, 2 for x, y, z
    if axis_type == 0:
        result = numpy.array(
            [[1, 0, 0], [0, numpy.cos(theta), -numpy.sin(theta)], [0, numpy.sin(theta), numpy.cos(theta)]])
    elif axis_type == 1:
        result = numpy.array(
            [[numpy.cos(theta), 0, numpy.sin(theta)], [0, 1, 0], [-numpy.sin(theta), 0, numpy.cos(theta)]])
    else:
        result = numpy.array(
            [[numpy.cos(theta), -numpy.sin(theta), 0], [numpy.sin(theta), numpy.cos(theta), 0], [0, 0, 1]])
    return result


euler_angle = numpy.matmul(numpy.matmul(get_rotation_matrix_of_axis(0.61, 1), get_rotation_matrix_of_axis(-3.07, 0)),
                           get_rotation_matrix_of_axis(-2.1, 2))


def get_skew_symmetric_mat(vec):
    result = numpy.array([[0, -vec[2, 0], vec[1, 0]], [vec[2, 0], 0, -vec[0, 0]], [-vec[1, 0], vec[0, 0], 0]])
    return result


def get_vector_from_skew_symmetric(mat):
    result = numpy.array([[mat[2, 1]], [mat[0, 2]], [mat[1, 0]]])
    return result


omega = numpy.array([[-0.36], [-1.01], [2.64]])
# HW3_result = numpy.matmul(numpy.matmul(numpy.matmul(R_1in0, get_skew_symmetric_mat(w_01in1)), R_1in0.T), R_1in0)
# HW3_result = get_skew_symmetric_mat(w_01in1)
# print("R_dot is: \n", HW3_result)


def rodrigues_form(axis_angle, theta):
    bracket_operator = get_skew_symmetric_mat(axis_angle)
    return numpy.identity(3) + numpy.sin(theta) * bracket_operator + (1 - numpy.cos(theta)) * numpy.matmul(bracket_operator, bracket_operator)


# w01 = numpy.array([[-0.21], [1.16], [-1.60]])
# t = 10.65
# rotation_angle = numpy.linalg.norm(w01)
# rotation_axis = w01 / rotation_angle
# HW3_problem3_result = rodrigues_form(rotation_axis, rotation_angle * t)


def log_of_rotation_matrix(rotation_mat):
    theta = numpy.arccos((numpy.matrix.trace(rotation_mat) - 1) / 2)
    axis = get_vector_from_skew_symmetric((rotation_mat - rotation_mat.T) / (2 * numpy.sin(theta)))
    return [axis, theta]


rot_mat = numpy.array([[0.65093810, -0.66366101, -0.36855618], [0.69554411, 0.32690008, 0.63980835], [-0.30413481, -0.67282271, 0.67439723]])
[hw3_5_result_axis, hw3_5_result_angle] = log_of_rotation_matrix(rot_mat)

R_1in0 = numpy.array([[0.99880318, -0.04370834, 0.02194972], [0.04665725, 0.98609619, -0.15949107], [-0.01467345, 0.16032430, 0.98695532]])
R_2in0 = numpy.array([[0.97010405, 0.20222396, 0.13417752], [-0.22808140, 0.94861503, 0.21933627], [-0.08292776, -0.24338240, 0.96637880]])
[result36_axis, result36_angle] = log_of_rotation_matrix(numpy.matmul(R_2in0.T, R_1in0))
# result36_axis = numpy.matmul(numpy.matmul(R_2in0.T, R_1in0), result36_axis)

R_1in0 = numpy.array([[-0.18685007, -0.13353350, -0.97327070], [0.73083368, -0.68094371, -0.04688061], [-0.65648243, -0.72005865, 0.22482516]])
w_01in1 = numpy.array([[-0.68697302], [-0.30906209], [0.14097058]])
hw34_result = numpy.matmul(R_1in0, -w_01in1)


R01 = numpy.array([[0.418555270341, 0.770432834293, 0.480879125678], [-0.483644164980, -0.259079447783, 0.836041961517], [0.768700076331, -0.582504152414, 0.264176276508]])
w0 = numpy.array([[0.210000000000], [-1.180000000000], [2.950000000000]])
t = 7.430000000000
p1 = numpy.array([[0.640000000000], [-2.870000000000], [0.000000000000]])

p0 = numpy.matmul(R01, p1)

rotation_angle = numpy.linalg.norm(w0)
rotation_axis = w0 / rotation_angle
# rotation_matrix = rodrigues_form(rotation_axis, t * rotation_angle)

rotation_matrix = numpy.matmul(rodrigues_form(rotation_axis, t * rotation_angle), R01)
result_position = numpy.matmul(rotation_matrix, p1)

# result_position = numpy.matmul(rotation_matrix.T, result_position)
# result_position = numpy.matmul(numpy.matmul(rodrigues_form(rotation_axis, t * rotation_angle), R01),  p1)
result_velocity = numpy.matmul(get_skew_symmetric_mat(w0), result_position)

# result_position = numpy.matmul(rotation_matrix.T, result_position)
# result_velocity = numpy.matmul(get_skew_symmetric_mat(numpy.matmul(R01, w1)), result_position) #求 p1(t), v1(t)

# result_velocity = numpy.matmul(rotation_matrix.T, result_velocity)
# tmpp = numpy.array([[1.3], [-2.51], [2.99]])


# numpy.matmul(R01, result_position) rotate with frame1 , require frame 0
# numpy.matmul(R01, result_velocity)