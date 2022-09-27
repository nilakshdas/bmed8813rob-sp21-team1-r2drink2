import os

import numpy as np
import pybullet as p

from assistive_gym.envs.agents.agent import Agent
from assistive_gym.envs.env import AssistiveEnv


CONTAINER_Y_POSITIONS = [3.6, 4, 4.4]
CONTAINER_COLORS = ["RED", "GREEN", "BLUE"]
COLOR_VALUES = dict(RED=[1, 0, 0, 1], GREEN=[0, 1, 0, 1], BLUE=[0, 0, 1, 1])


def create_hydration_container(env: AssistiveEnv, pos: list, color: list) -> Agent:
    visual_filename = os.path.join(
        env.directory, "dinnerware", "plastic_coffee_cup.obj"
    )
    collision_filename = os.path.join(
        env.directory, "dinnerware", "plastic_coffee_cup_vhacd.obj"
    )

    mass = 0.1
    mesh_scale = [0.05] * 3

    orient = [0, 0, 0, 1]

    tool_visual = p.createVisualShape(
        shapeType=p.GEOM_MESH,
        fileName=visual_filename,
        meshScale=mesh_scale,
        rgbaColor=color,
        physicsClientId=env.id,
    )
    tool_collision = p.createCollisionShape(
        shapeType=p.GEOM_MESH,
        fileName=collision_filename,
        meshScale=mesh_scale,
        physicsClientId=env.id,
    )
    tool = p.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=tool_collision,
        baseVisualShapeIndex=tool_visual,
        basePosition=pos,
        baseOrientation=orient,
        useMaximalCoordinates=False,
        physicsClientId=env.id,
    )

    tool_agent = Agent()
    tool_agent.init(tool, env.id, env.np_random, indices=-1)
    return tool_agent


def setup_hydration_staging(env: AssistiveEnv):
    positions = np.array(CONTAINER_Y_POSITIONS)
    colors = np.array(CONTAINER_COLORS)

    env.np_random.shuffle(colors)
    env.np_random.shuffle(positions)

    for y, color in zip(positions.tolist(), colors.tolist()):
        pos = [-3.8, y, 0.9]
        col = COLOR_VALUES[color]
        create_hydration_container(env, pos, col)

    print(env.np_random.choice(colors))
