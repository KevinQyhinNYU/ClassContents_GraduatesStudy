import matplotlib.pyplot as plt
from myRoboticsComputation import *

robot = RoboticArm("Kuka_iiwa_14", 7, [0, 0, 1.301])
Spatial_Screw_Axises = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, -1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1],
                                 [0, -0.36, 0, 0.78, 0, -1.18, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
robot.initialize_screw_axis(Spatial_Screw_Axises)

with open('desired_end_effector_positions.npy', 'rb') as f:
    desired_endeff = np.load(f)

test_position = desired_endeff[:, [1]]
# robot.configurations = np.array([1.93933984, -0.99692222, 1.35182754, 0.02439171, 0.9996885, 0.03332622, 1.])
[theta_list, iter_num1] = robot.compute_inverse_kinematics_positions(test_position)
ik_solution = theta_list[-1]

# third_frame = get_transformation_matrix_from_rotation_and_translation(np.identity(3), test_position)
# robot.compute_spatial_jacobian(robot.configurations)
# jacobian_s = robot.get_spatial_jacobian()
# jacobian_new = np.matmul(get_adjoint_representation_of_transformation(get_inverse_of_transformation(third_frame)), jacobian_s)
# jacobian_x_part = jacobian_new[3:6, :]
# jacobian_pinv = np.linalg.pinv(jacobian_x_part)
#
# robot.configurations = np.matmul(jacobian_pinv, test_position)
# robot.forward_kinematics(robot.configurations)
robot.forward_kinematics(ik_solution)
validating_ans = robot.get_end_effector_pose()
[r1, t1] = get_rotation_and_translation_from_transform_matrix(validating_ans)
print("error1 is: ", np.linalg.norm(test_position - t1))
print("iter1 is: ", iter_num1)

norm_list = []
for i in range(desired_endeff.shape[1]):
    # print("Norm is: \n", np.linalg.norm(desired_endeff[:, [i]]))
    norm_list.append(np.linalg.norm(desired_endeff[:, [i]]))

# [ik_solution_regularization, iter_num2] = robot.ik_solution_regularization_method(test_position)
# robot.forward_kinematics(ik_solution_regularization)
# validating_ans2 = robot.get_end_effector_pose()
# [r2, t2] = get_rotation_and_translation_from_transform_matrix(validating_ans2)
# print("error2 is: ", np.linalg.norm(test_position - t2))
# print("iter2 is: ", iter_num2)

desired_configurations = np.array([1, 1, -1, -1, 1, 1, 1])
desired_configurations = np.resize(desired_configurations, (7, 1))

[theta_list_2, iter_num2] = robot.ik_solution_with_nullspace(test_position, desired_configurations)
new_ik_solution = theta_list_2[-1]

robot.forward_kinematics(new_ik_solution)
validating_ans2 = robot.get_end_effector_pose()
[r2, t2] = get_rotation_and_translation_from_transform_matrix(validating_ans2)
print("\nerror2 is: ", np.linalg.norm(test_position - t2))
print("iter2 is: ", iter_num2)

