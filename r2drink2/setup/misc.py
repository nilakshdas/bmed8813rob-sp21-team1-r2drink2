import os
import numpy as np
import pybullet as p

from assistive_gym.envs.env import AssistiveEnv


def setup_plane(env: AssistiveEnv):
    plane = p.loadURDF(
        os.path.join(env.directory, "plane", "plane.urdf"), physicsClientId=env.id
    )

    env.plane.init(plane, env.id, env.np_random, indices=-1)

    env.plane.set_frictions(
        env.plane.base,
        lateral_friction=env.np_random.uniform(0.025, 0.5),
        spinning_friction=0,
        rolling_friction=0,
    )
