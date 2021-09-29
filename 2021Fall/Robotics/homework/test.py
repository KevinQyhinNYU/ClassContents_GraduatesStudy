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

T_04 = numpy.array([[0.93206637, 0.27038449, -0.24113171, -0.82928384], [0.16835921, 0.26608178, 0.94913416, 0.45283116],
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


T_8in0 = numpy.array([[0.42734620, -0.52768407, 0.73411494, -0.15899131], [-0.90189692, -0.30532058, 0.30555081, 0.24010015], [0.06290610, -0.79267198, -0.60639423, 0.90700601], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
T_6in8 = numpy.array([[-0.77961294, -0.57815721, -0.24070293, -0.14187170], [0.00816554, 0.37493194, -0.92701638, -0.10927903], [0.62620842, -0.72467944, -0.28758083, -0.54832063], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])

pose_6in0 = numpy.matmul(T_8in0, T_6in8)



def get_rotation_matrix_of_axis(theta, axis_type): # 0, 1, 2 for x, y, z
    if axis_type == 0:
        result = numpy.array([[1, 0, 0], [0, numpy.cos(theta), -numpy.sin(theta)], [0, numpy.sin(theta), numpy.cos(theta)]])
    elif axis_type == 1:
        result = numpy.array([[numpy.cos(theta), 0, numpy.sin(theta)], [0, 1, 0], [-numpy.sin(theta), 0, numpy.cos(theta)]])
    else:
        result = numpy.array([[numpy.cos(theta), -numpy.sin(theta), 0], [numpy.sin(theta), numpy.cos(theta), 0], [0, 0, 1]])
    return result


euler_angle = numpy.matmul(numpy.matmul(get_rotation_matrix_of_axis(0.61, 1), get_rotation_matrix_of_axis(-3.07, 0)),
                               get_rotation_matrix_of_axis(-2.1, 2))
