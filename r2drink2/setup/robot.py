import numpy as np

from assistive_gym.envs.env import AssistiveEnv

from r2drink2.agents.stretch import TeleOpStretch


def setup_robot(env: AssistiveEnv):
    robot = env.create_robot(
        TeleOpStretch, controllable_joints="wheel_right", fixed_base=False
    )

    pos = [-3, 4, 0.1]
    orient = [0, 0, -np.pi / 2.0]
    robot.set_base_pos_orient(pos, orient)

    return robot
