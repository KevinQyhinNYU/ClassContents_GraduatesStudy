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
    linear_velocity = twist_bracket[0:3, [3]]
    angular_velocity = np.array([[twist_bracket[2, 1]], [twist_bracket[0, 2]], [twist_bracket[1, 0]]])

    result = np.append(angular_velocity, linear_velocity, axis=0)
    return result


def get_adjoint_representation_of_transformation(transformation):
    [rotation, translation] = get_rotation_and_translation_from_transform_matrix(transformation)
    zero_mat = np.zeros((3, 3))

    adjoint_mat = np.append(np.append(rotation, zero_mat, axis=1),
                            np.append(np.matmul(get_skew_symmetric_mat(translation), rotation), rotation, axis=1), axis=0)
    return adjoint_mat


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


class RoboticArm:
    name = ""
    degree_Of_FreeDom = 0
    initial_position = []  # Position of end effector at zero-configuration
    configurations = []
    spatial_screw_axis = []

    endEffector_pose = np.identity(4)
    spatial_Jacobian = np.array([[], [], [], [], [], []])

    def __init__(self, name_string, dof, starting_position):
        self.name = name_string
        self.degree_Of_FreeDom = dof
        self.configurations = np.zeros(dof)
        self.initial_position = starting_position

    def get_end_effector_pose(self):
        return self.endEffector_pose

    def initialize_screw_axis(self, axis: np.array):
        if axis.shape[0] != 6:
            print("The dimension of single screw axis should be 6!!!")

        if axis.shape[1] != self.degree_Of_FreeDom:
            print("The number of input Screw axes does not match the DOF of the Robot!!!")

        for i in range(self.degree_Of_FreeDom):
            self.spatial_screw_axis.append(axis[:, [i]])

    def forward_kinematics(self, theta: np.array):
        axes = self.spatial_screw_axis.copy()
        initial_translation = np.resize(self.initial_position, (3, 1))
        self.endEffector_pose = get_transformation_matrix_from_rotation_and_translation(np.identity(3), initial_translation)

        for i in range(self.degree_Of_FreeDom):
            screw_axis = axes.pop()
            self.endEffector_pose = np.matmul(exp_of_twist_vector(screw_axis * theta[self.degree_Of_FreeDom - i - 1]),
                                              self.endEffector_pose)

    def get_spatial_jacobian(self):
        return self.spatial_Jacobian

    def compute_spatial_jacobian(self, theta: np.array):
        self.spatial_Jacobian = np.array([[], [], [], [], [], []])
        axes = self.spatial_screw_axis.copy()
        multi_mat = np.identity(4)

        for i in range(self.degree_Of_FreeDom):
            screw_axis = axes[i]
            Jacobian_i = np.matmul(get_adjoint_representation_of_transformation(multi_mat), screw_axis)
            self.spatial_Jacobian = np.append(self.spatial_Jacobian, Jacobian_i, axis=1)

            if i != self.degree_Of_FreeDom - 1:
                multi_mat = np.matmul(multi_mat, exp_of_twist_vector(screw_axis * theta[i]))

    def compute_inverse_kinematics_positions(self, desired_position):
        configuration_list = []
        self.configurations = np.zeros(self.degree_Of_FreeDom)
        configuration_list.append(self.configurations)
        epsilon = 0.0001
        epsilon2 = 0.000001
        learning_rate = 1
        iter_num = 1

        self.forward_kinematics(self.configurations)
        [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())
        last_trans = trans - 1

        if np.linalg.norm(desired_position) > np.linalg.norm(self.initial_position):
            while np.linalg.norm(trans - last_trans) > epsilon:
                last_trans = trans
                self.compute_spatial_jacobian(self.configurations)
                jacobian_s = self.get_spatial_jacobian()
                third_frame = get_transformation_matrix_from_rotation_and_translation(np.identity(3), trans)
                jacobian_new = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(third_frame)), jacobian_s)
                jacobian_x_part = jacobian_new[3:6, :]

                delta_theta = np.matmul(jacobian_x_part.T, desired_position - trans)
                delta_theta = np.resize(delta_theta, (self.degree_Of_FreeDom,))
                self.configurations = self.configurations + learning_rate * delta_theta
                configuration_list.append(self.configurations)

                self.forward_kinematics(self.configurations)
                [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())
                # print("\n\nIteration No. \n", iter_num)
                # print("Joint is: \n", self.configurations)
                # print("Error is: \n", np.linalg.norm(trans - desired_position))
                iter_num = iter_num + 1
        else:
            while np.linalg.norm(trans - desired_position) > epsilon2:
                self.compute_spatial_jacobian(self.configurations)
                jacobian_s = self.get_spatial_jacobian()
                third_frame = get_transformation_matrix_from_rotation_and_translation(np.identity(3), trans)
                jacobian_new = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(third_frame)), jacobian_s)
                jacobian_x_part = jacobian_new[3:6, :]
                jacobian_pinv = np.linalg.pinv(jacobian_x_part)

                delta_theta = np.matmul(jacobian_pinv, desired_position - trans)
                delta_theta = np.resize(delta_theta, (self.degree_Of_FreeDom, ))
                self.configurations = self.configurations + learning_rate * delta_theta
                configuration_list.append(self.configurations)

                self.forward_kinematics(self.configurations)
                [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())
                # print("\n\nIteration No. \n", iter_num)
                # print("Joint is: \n", self.configurations)
                # print("Error is: \n", np.linalg.norm(trans - desired_position))
                iter_num = iter_num + 1

        return [configuration_list, iter_num]

    def ik_solution_regularization_method(self, desired_position):
        configuration_list = []
        self.configurations = np.zeros(self.degree_Of_FreeDom)
        configuration_list.append(self.configurations)
        epsilon = 0.000001
        learning_rate = 1
        iter_num = 1
        lambda_coef = 0.1

        self.forward_kinematics(self.configurations)
        [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())

        while np.linalg.norm(trans - desired_position) > epsilon:
            self.compute_spatial_jacobian(self.configurations)
            jacobian_s = self.get_spatial_jacobian()
            third_frame = get_transformation_matrix_from_rotation_and_translation(np.identity(3), trans)
            jacobian_new = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(third_frame)), jacobian_s)
            jacobian_x_part = jacobian_new[3:6, :]
            J_mat = np.matmul(jacobian_x_part.T, np.linalg.inv(np.matmul(jacobian_x_part, jacobian_x_part.T) + lambda_coef * np.identity(jacobian_x_part.shape[0])))

            delta_theta = np.matmul(J_mat, desired_position - trans)
            delta_theta = np.resize(delta_theta, (self.degree_Of_FreeDom,))
            self.configurations = self.configurations + learning_rate * delta_theta
            configuration_list.append(self.configurations)

            self.forward_kinematics(self.configurations)
            [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())
            # print("\n\nIteration No. \n", iter_num)
            # print("Joint is: \n", self.configurations)
            # print("Error is: \n", np.linalg.norm(trans - desired_position))
            iter_num = iter_num + 1

        return [self.configurations, iter_num]

    def ik_solution_with_nullspace(self, desired_position, desired_configuration):
        configuration_list = []
        self.configurations = np.zeros(self.degree_Of_FreeDom)
        # self.configurations = desired_configuration
        configuration_list.append(self.configurations)
        epsilon = 0.0001
        epsilon2 = 0.01
        learning_rate = 0.1
        iter_num = 1

        self.forward_kinematics(self.configurations)
        [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())
        last_trans = trans - 1

        while np.linalg.norm(trans - last_trans) > epsilon:
        # while np.linalg.norm(trans - desired_position) > epsilon2:
            last_trans = trans
            self.compute_spatial_jacobian(self.configurations)
            jacobian_s = self.get_spatial_jacobian()
            third_frame = get_transformation_matrix_from_rotation_and_translation(np.identity(3), trans)
            jacobian_new = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(third_frame)), jacobian_s)
            jacobian_x_part = jacobian_new[3:6, :]
            jacobian_pinv = np.linalg.pinv(jacobian_x_part)

            null_space_projection_mat = np.identity(jacobian_x_part.shape[1]) - np.matmul(jacobian_pinv, jacobian_x_part)
            delta_theta = np.matmul(jacobian_pinv, desired_position - trans) + np.matmul(null_space_projection_mat, desired_configuration - self.configurations)

            delta_theta = np.resize(delta_theta, (self.degree_Of_FreeDom,))
            self.configurations = self.configurations + learning_rate * delta_theta
            configuration_list.append(self.configurations)

            self.forward_kinematics(self.configurations)
            [rot, trans] = get_rotation_and_translation_from_transform_matrix(self.get_end_effector_pose())
            # print("\n\nIteration No. \n", iter_num)
            # print("Joint is: \n", self.configurations)
            # print("Error is: \n", np.linalg.norm(trans - desired_position))
            iter_num = iter_num + 1

        return [configuration_list, iter_num]

