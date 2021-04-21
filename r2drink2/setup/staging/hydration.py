import os

import pybullet as p

from assistive_gym.envs.agents.agent import Agent
from assistive_gym.envs.env import AssistiveEnv


def create_hydration_container(env: AssistiveEnv) -> Agent:
    visual_filename = os.path.join(
        env.directory, "dinnerware", "plastic_coffee_cup.obj"
    )
    collision_filename = os.path.join(
        env.directory, "dinnerware", "plastic_coffee_cup_vhacd.obj"
    )

    mass = 0.1
    mesh_scale = [0.05] * 3

    pos = [-3.8, 4.2, 0.9]
    orient = [0, 0, 0, 1]

    tool_visual = p.createVisualShape(
        shapeType=p.GEOM_MESH,
        fileName=visual_filename,
        meshScale=mesh_scale,
        rgbaColor=[1, 0, 0, 1],
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
    create_hydration_container(env)
