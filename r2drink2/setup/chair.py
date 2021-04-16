import numpy as np

from assistive_gym.envs.agents.agent import Agent
from assistive_gym.envs.env import AssistiveEnv


def setup_chair(env: AssistiveEnv):
    env.furniture.init(
        "wheelchair",
        env.directory,
        env.id,
        env.np_random,
        wheelchair_mounted=False,
    )

    pos, orient = env.furniture.get_base_pos_orient()
    env.furniture.set_base_pos_orient(pos + np.array([-0.5, 0, 0]), orient)
