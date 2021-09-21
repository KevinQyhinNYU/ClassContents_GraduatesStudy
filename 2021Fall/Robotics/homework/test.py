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

T_04 = numpy.array([[-0.04487593, -0.01604671, 0.99886368, -0.54945160], [0.77277141, 0.63309504, 0.04488894, 0.66528422], [-0.63309597, 0.77390773, -0.01601028, -0.33452981], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
p_4 = numpy.array([[0.34722157], [0.09087700], [0.75403028], [0.0]])
p_0 = numpy.matmul(numpy.linalg.inv(T_04), p_4)
print("p_0 is : \n", p_0)
print("\n")

M = numpy.matrix([[2], [2]])
print(get_rotation_matrix(numpy.pi / 6.0) * M)
