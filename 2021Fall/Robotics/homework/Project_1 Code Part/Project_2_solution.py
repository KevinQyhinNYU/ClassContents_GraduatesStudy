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

    ik_solution = theta_list[-1]

    robot.forward_kinematics(ik_solution)
    validating_ans = robot.get_end_effector_pose()
    [r1, t1] = get_rotation_and_translation_from_transform_matrix(validating_ans)
    print("error is: ", np.linalg.norm(test_position - t1))
    print("iter is: ", iter_num1)


robot = RoboticArm("Kuka_iiwa_14", 7, [0, 0, 1.301])
Spatial_Screw_Axises = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, -1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1],
                                 [0, -0.36, 0, 0.78, 0, -1.18, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
robot.initialize_screw_axis(Spatial_Screw_Axises)

with open('desired_end_effector_positions.npy', 'rb') as f:
    desired_endeff = np.load(f)


selected_data = desired_endeff[:, [0]]
test_unit(selected_data, "normal")
test_unit(selected_data, "regularized")


# Check if the goal position could be reached
norm_list = []
for i in range(desired_endeff.shape[1]):
    # print("Norm is: \n", np.linalg.norm(desired_endeff[:, [i]]))
    norm_list.append(np.linalg.norm(desired_endeff[:, [i]]))

desired_configurations = np.array([1, 1, -1, -1, 1, 1, 1])
desired_configurations = np.resize(desired_configurations, (7, 1))

[theta_list, iter_num1] = robot.ik_solution_regularization_method(selected_data, desired_configurations)
ik_solution = theta_list[-1]

robot.forward_kinematics(ik_solution)
validating_ans = robot.get_end_effector_pose()
[r1, t1] = get_rotation_and_translation_from_transform_matrix(validating_ans)
print("error1 is: ", np.linalg.norm(selected_data - t1))
print("iter1 is: ", iter_num1)
