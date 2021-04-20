import numpy as np

from assistive_gym.envs.agents.stretch import Stretch
from assistive_gym.envs.env import AssistiveEnv


def setup_robot(env: AssistiveEnv):
    robot = env.create_robot(
        Stretch, controllable_joints="wheel_right", fixed_base=False
    )

    pos = [0.5, -1, 0.1]
    orient = [0, 0, np.pi / 2.0]
    robot.set_base_pos_orient(pos, orient)

    return robot
