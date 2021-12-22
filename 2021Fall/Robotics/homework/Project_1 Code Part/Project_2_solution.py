import matplotlib.pyplot as plt
from myRoboticsComputation import *


def normalize_joint_configuration(theta: np.array):
    for i in range(theta.shape[0]):
        if theta[i] > np.pi or theta[i] < -np.pi:
            while theta[i] > np.pi:
                theta[i] -= 2 * np.pi

            while theta[i] < -np.pi:
                theta[i] += 2 * np.pi
    return theta


def test_unit(test_data, method):
    test_position = test_data

    if method == "normal":
        [theta_list, iter_num1] = robot.compute_inverse_kinematics_positions(test_position)
    elif method == "regularized":
        [theta_list, iter_num1] = robot.ik_solution_regularization_method(test_position)
    elif method == "revised":
        [ik_solution, iter_num1] = robot.compute_IK_position(test_position)

    if method != "revised":
        ik_solution = theta_list[-1]

    robot.forward_kinematics(ik_solution)
    validating_ans = robot.get_end_effector_pose()
    [r1, t1] = get_rotation_and_translation_from_transform_matrix(validating_ans)
    print("Method is: ", method)
    print("error is: ", np.linalg.norm(test_position - t1))
    print("iter is: ", iter_num1)


robot = RoboticArm("Kuka_iiwa_14", 7, [0, 0, 1.301])
Spatial_Screw_Axises = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, -1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1],
                                 [0, -0.36, 0, 0.78, 0, -1.18, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
robot.initialize_screw_axis(Spatial_Screw_Axises)

with open('desired_end_effector_positions.npy', 'rb') as f:
    desired_endeff = np.load(f)


selected_data = desired_endeff[:, [7]]
# test_unit(selected_data, "normal")
test_unit(selected_data, "regularized")
test_unit(selected_data, "revised")

# Check if the goal position could be reached
norm_list = []
for i in range(desired_endeff.shape[1]):
    # print("Norm is: \n", np.linalg.norm(desired_endeff[:, [i]]))
    norm_list.append(np.linalg.norm(desired_endeff[:, [i]]))

desired_configurations = np.array([1, 1, -1, -1, 1, 1, 1])
desired_configurations = np.resize(desired_configurations, (7, 1))

[ik_solution, iter_num1] = robot.compute_IK_position_nullspace(selected_data, desired_configurations)
ik_solution = normalize_joint_configuration(ik_solution)

robot.forward_kinematics(ik_solution)
validating_ans = robot.get_end_effector_pose()
[r1, t1] = get_rotation_and_translation_from_transform_matrix(validating_ans)
print("error1 is: ", np.linalg.norm(selected_data - t1))
print("iter1 is: ", iter_num1)

M = np.array([[-0.62938175, -0.43657478, 0.64286940, -2.64180803], [-0.34944977, 0.89791139, 0.26765649, -0.94732414], [-0.69409183, -0.05619245, -0.71769000, 0.02189382], [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
V_b = np.array([[0.61093402], [0.01265028], [-0.82493961], [-0.85938570], [-0.66997692], [0.15096138]])
V_s = np.matmul(get_adjoint_representation_of_transformation(M), V_b)
hw4_3_result = np.matmul(M, exp_of_twist_vector(V_b))
