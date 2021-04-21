import numpy as np

from assistive_gym.envs.agents.agent import Agent
from assistive_gym.envs.env import AssistiveEnv


CHAIR_Z_POS = 0.06
CHAIR_POSITIONS = [np.array([2, 3, CHAIR_Z_POS])]


def setup_chair(env: AssistiveEnv):
    env.furniture.init(
        "wheelchair",
        env.directory,
        env.id,
        env.np_random,
        wheelchair_mounted=False,
    )

    _, orient = env.furniture.get_base_pos_orient()
    pos = CHAIR_POSITIONS[env.np_random.choice(np.arange(len(CHAIR_POSITIONS)))]
    env.furniture.set_base_pos_orient(pos, orient)
