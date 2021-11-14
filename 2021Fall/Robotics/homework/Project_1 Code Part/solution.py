import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from myRoboticsComputation import *


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

    def forward_kinematics_computing(self, theta: np.array):
        axes = self.spatial_screw_axis.copy()
        initial_translation = np.resize(self.initial_position, (3, 1))
        self.endEffector_pose = get_transformation_matrix_from_rotation_and_translation(np.identity(3), initial_translation)

        for i in range(self.degree_Of_FreeDom):
            screw_axis = axes.pop()
            self.endEffector_pose = np.matmul(exp_of_twist_vector(screw_axis * theta[self.degree_Of_FreeDom - i - 1]),
                                              self.endEffector_pose)

    def get_spatial_Jacobian(self, theta: np.array):
        self.spatial_Jacobian = np.array([[], [], [], [], [], []])
        axes = self.spatial_screw_axis.copy()
        multi_mat = np.identity(4)

        for i in range(self.degree_Of_FreeDom):
            screw_axis = axes[i]
            Jacobian_i = np.matmul(get_adjoint_representation_of_transformation(multi_mat), screw_axis)
            self.spatial_Jacobian = np.append(self.spatial_Jacobian, Jacobian_i, axis=1)

            if i != self.degree_Of_FreeDom - 1:
                multi_mat = np.matmul(multi_mat, exp_of_twist_vector(screw_axis * theta[i]))

        return self.spatial_Jacobian


robot = RoboticArm("Kuka_iiwa_14", 7, [0, 0, 1.301])
Spatial_Screw_Axises = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, -1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1],
                                 [0, -0.36, 0, 0.78, 0, -1.18, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
robot.initialize_screw_axis(Spatial_Screw_Axises)

# np.array([-0.69653, -0.59870, -0.12313, 1.30247, -0.01196, -0.37886, 0.00000])
# np.array([-1.2, 0.7, 2.8, 0.7, 1.2, 0.2, 0.3])
theta_configurations = np.array([-1.2, 0.7, 2.8, 0.7, 1.2, 0.2, 0.3])
robot.forward_kinematics_computing(theta_configurations)
print("End effctor pose is: \n", robot.get_end_effector_pose())
print("\nCurrent Spatial Jacobian is: \n", robot.get_spatial_Jacobian(theta_configurations))

# Question 4:

with open('joint_trajectory.npy', 'rb') as f:
    joint_trajectory = np.load(f)

num_of_configurations = joint_trajectory.shape[1]
# endEffector_position_list = []
# for i in range(num_of_configurations):
#     theta = joint_trajectory[:, i]
#     robot.forward_kinematics_computing(theta)
#     [rot, trans] = get_rotation_and_translation_from_transform_matrix(robot.get_end_effector_pose())
#     endEffector_position_list.append(trans)
#
# x_pos_list = []
# y_pos_list = []
# z_pos_list = []
#
#
# for i in range(num_of_configurations):
#     x_pos_list.append(endEffector_position_list[i][0, 0])
#     y_pos_list.append(endEffector_position_list[i][1, 0])
#     z_pos_list.append(endEffector_position_list[i][2, 0])
#
# plt.figure(figsize=(25, 16))
#
# plt.subplot(1, 3, 1)
# plt.plot(x_pos_list, y_pos_list)
# plt.xlabel("x-axis position", fontsize=20)
# plt.xticks(fontsize=15)
# plt.ylabel("y-axis position", fontsize=20)
# plt.yticks(fontsize=15)
# plt.title("X vs Y")
# plt.grid()
#
# plt.subplot(1, 3, 2)
# plt.plot(x_pos_list, z_pos_list)
# plt.title("X vs Z")
# plt.grid()
#
# plt.subplot(1, 3, 3)
# plt.plot(y_pos_list, z_pos_list)
# plt.title("Y vs Z")
# plt.grid()
#
# plt.show()

# Question 5
with open('joint_velocity.npy', 'rb') as f:
    joint_velocities = np.load(f)

x_linear_v_list = []
y_linear_v_list = []
z_linear_v_list = []

for i in range(num_of_configurations):
    theta = joint_trajectory[:, i]
    dtheta = joint_velocities[:, [i]]
    current_spatial_jacobian = robot.get_spatial_Jacobian(theta)
    current_spatial_twist_of_endEffector = np.matmul(current_spatial_jacobian, dtheta)
    [angular_velocity, linear_velocity] = get_angular_velocity_and_linear_velocity_from_twist_vector(current_spatial_twist_of_endEffector)
    x_linear_v_list.append(linear_velocity[0])
    y_linear_v_list.append(linear_velocity[1])
    z_linear_v_list.append(linear_velocity[2])

plt.figure(figsize=(25, 16))

t_series = range(num_of_configurations)

plt.subplot(3, 1, 1)
# plt.plot(x_linear_v_list, x_linear_v_list)
plt.plot(t_series, x_linear_v_list)
plt.xlabel("x-axis position", fontsize=20)
plt.xticks(fontsize=15)
plt.ylabel("y-axis position", fontsize=20)
plt.yticks(fontsize=15)
plt.title("X linear v")
plt.grid()

plt.subplot(3, 1, 2)
# plt.plot(x_linear_v_list, z_linear_v_list)
plt.plot(t_series, y_linear_v_list)
plt.title("Y linear v")
plt.grid()

plt.subplot(3, 1, 3)
# plt.plot(y_linear_v_list, z_linear_v_list)
plt.plot(t_series, z_linear_v_list)
plt.title("Z linear v")
plt.grid()

plt.show()
