import numpy as np

from assistive_gym.envs.agents.agent import Agent
from assistive_gym.envs.env import AssistiveEnv


CHAIR_Z_POS = 0.06
CHAIR_POSITIONS = [
    ("bedroom1", np.array([4, 4, CHAIR_Z_POS]), 0),
    ("bedroom2", np.array([4, -4, CHAIR_Z_POS]), -np.pi),
    ("bathroom", np.array([1, -4, CHAIR_Z_POS]), -np.pi / 2),
    ("closet", np.array([-4, -3, CHAIR_Z_POS]), 0),
    ("living", np.array([0, 4, CHAIR_Z_POS]), -np.pi / 2),
    ("kitchen", np.array([-4, -1, CHAIR_Z_POS]), -np.pi),
]


def setup_chair(env: AssistiveEnv):
    env.furniture.init(
        "wheelchair", env.directory, env.id, env.np_random, wheelchair_mounted=False
    )

    _, orient = env.furniture.get_base_pos_orient()

    room_index = env.np_random.choice(np.arange(len(CHAIR_POSITIONS)))
    room, pos, yaw = CHAIR_POSITIONS[room_index]
    orient = env.get_quaternion(env.get_euler(orient) + np.array([0, 0, yaw]))

    env.furniture.set_base_pos_orient(pos, orient)

    print(room)
