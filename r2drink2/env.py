from gibson2.scenes.igibson_indoor_scene import InteractiveIndoorScene

import assistive_gym
from assistive_gym.envs.env import AssistiveEnv
from assistive_gym.envs.agents.pr2 import PR2
from assistive_gym.envs.agents.stretch import Stretch
from assistive_gym.envs.agents.agent import Agent
import assistive_gym.envs.agents.human as h

import pybullet as p
import numpy as np
import time
from numpngw import write_apng
from IPython.display import Image

# Create an empty Assistive Gym environment
env = AssistiveEnv()
env.set_seed(200)
# env.setup_camera(camera_eye=[1.5, -2, 2], camera_target=[-0.6, -0.5, 0.7], fov=60, camera_width=1920//4, camera_height=1080//4)
env.setup_camera(camera_eye=[1.75, -1.5, 2], camera_target=[-0.6, -0.25, 0.4], fov=60, camera_width=1920//4, camera_height=1080//4)
env.reset()

# Create the iGibson environment
scene = InteractiveIndoorScene('Rs_int', build_graph=True, pybullet_load_texture=True, texture_randomization=False, object_randomization=False)
scene.load()

# Change position of a chair (the 15th object)
chair = Agent()
chair.init_env(15, env, indices=-1)
pos, orient = chair.get_base_pos_orient()
chair.set_base_pos_orient(pos + np.array([-0.5, 0, 0]), orient)

# Create human
human = env.create_human(controllable=False, controllable_joint_indices=h.right_arm_joints, fixed_base=False,
                         human_impairment='none', gender='random', mass=None, radius_scale=1.0, height_scale=1.0)
# Define the initial pose for the human
joints_positions = [(human.j_right_elbow, -90), (human.j_left_elbow, -90), (human.j_right_hip_x, -80),
                    (human.j_right_knee, 80), (human.j_left_hip_x, -80), (human.j_left_knee, 80)]
human.setup_joints(joints_positions, use_static_joints=False, reactive_force=None, reactive_gain=0.05)
# Set human on chair and increase body friction
chair_pos, chair_orient = chair.get_base_pos_orient()
human.set_base_pos_orient(chair_pos + np.array([0.01, 0, -0.5 + (0.89 if human.gender == 'male' else 0.86)]),
                          env.get_quaternion(env.get_euler(chair_orient) + np.array([-0.1, 0, 0])))
human.set_whole_body_frictions(lateral_friction=10, spinning_friction=10, rolling_friction=10)
# Stiffen the joints so they do not fall limp so easily
human.set_all_joints_stiffness(0.01)

# Create robot
robot = env.create_robot(Stretch, controllable_joints='wheel_right', fixed_base=False)
# robot.print_joint_info()
robot.set_base_pos_orient([0.5, -1, 0.1], [0, 0, np.pi/2.0])

# frames = []
# done = False
# for _ in range(60):
#     action = np.zeros(len(env.robot.controllable_joint_indices))
#     action[:len(env.robot.wheel_joint_indices)+1] = 1.0
#     # observation, reward, done, info = env.step(action)
#     env.take_step(action)
#     img, depth = env.get_camera_image_depth()
#     frames.append(img)
# env.disconnect()
# write_apng('output.png', frames, delay=100)

# env.render()
# while True:
#     time.sleep(0.5)
#     print("step")
#     action = np.zeros(len(env.robot.controllable_joint_indices))
#     env.take_step(action)

env.setup_camera(
    fov=60,
    camera_eye=[0.5, -1, 0.1],
    camera_target=[-0.5, 0, 0.75],
    camera_width=1920 // 4,
    camera_height=1080 // 4,
)

env.render()
env.reset()
while True:
    action = np.zeros(len(env.robot.controllable_joint_indices))
    # action[:len(env.robot.wheel_joint_indices)+1] = 1.0
    # observation, reward, done, info = env.step(action)
    env.take_step(action)
    # img, depth = env.get_camera_image_depth()
    # frames.append(img)
    time.sleep(0.5)
    print("step")
env.disconnect()