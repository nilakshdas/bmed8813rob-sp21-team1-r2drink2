from assistive_gym.envs.agents.furniture import Furniture
from assistive_gym.envs.env import AssistiveEnv


def setup_table(env: AssistiveEnv):
    table = Furniture()
    table.init("table", env.directory, env.id, env.np_random)
    table.set_base_pos_orient(pos=[-4, 4, 0], orient=[0, 0, 1, 1])
