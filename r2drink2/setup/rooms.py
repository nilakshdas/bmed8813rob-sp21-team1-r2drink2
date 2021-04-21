from dataclasses import dataclass
from enum import Enum
from typing import List

import numpy as np
import pybullet as p

from assistive_gym.envs.agents.agent import Agent
from assistive_gym.envs.env import AssistiveEnv


@dataclass
class PointXY:
    x: float
    y: float


class ROOM_OPENINGS:
    NW_TOP = "NW_TOP"
    NW_LEFT = "NW_LEFT"
    NE_TOP = "NE_TOP"
    NE_RIGHT = "NE_RIGHT"
    SE_BOTTOM = "SE_BOTTOM"
    SE_RIGHT = "SE_RIGHT"
    SW_BOTTOM = "SW_BOTTOM"
    SW_LEFT = "SW_LEFT"


ROOM_CONFIGS = {
    "staging_area": dict(
        sw_pos=PointXY(-5, -5),
        ne_pos=PointXY(-3, -3),
        openings=[ROOM_OPENINGS.NE_TOP, ROOM_OPENINGS.SE_RIGHT],
    ),
    "room1": dict(
        sw_pos=PointXY(-3, -5),
        ne_pos=PointXY(-1, -1),
        openings=[ROOM_OPENINGS.SW_LEFT, ROOM_OPENINGS.NE_TOP, ROOM_OPENINGS.SE_RIGHT],
    ),
    #  "room2": dict(
    #      sw_pos=PointXY(-1, -5),
    #      ne_pos=PointXY(2, -1),
    #      openings=[ROOM_OPENINGS.SW_LEFT, ROOM_OPENINGS.NE_TOP],
    #  ),
}

WALL_WIDTH = 0.1
WALL_HEIGHT = 2
OPENING_LENGTH = 0.8
MIN_WALL_LENGTH = (2 * OPENING_LENGTH) + 0.1


def create_wall(
    env: AssistiveEnv,
    sw_pos: PointXY,
    wall_length: float,
    lateral_orientation: bool,
):
    transverse_orientation = not lateral_orientation

    wall_dim_x = wall_length / 2 if lateral_orientation else WALL_WIDTH / 2
    wall_dim_y = wall_length / 2 if transverse_orientation else WALL_WIDTH / 2
    wall_dim_z = WALL_HEIGHT / 2

    wall_extents = [wall_dim_x, wall_dim_y, wall_dim_z]
    wall_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=wall_extents)
    wall_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=wall_extents)

    pos = np.zeros(3)
    pos[0] = sw_pos.x + wall_dim_x
    pos[1] = sw_pos.y + wall_dim_y
    pos[2] = wall_dim_z

    wall_body = p.createMultiBody(
        baseMass=0.0,
        baseCollisionShapeIndex=wall_collision,
        baseVisualShapeIndex=wall_visual,
        basePosition=pos,
        useMaximalCoordinates=False,
        physicsClientId=env.id,
    )

    wall_agent = Agent()
    wall_agent.init(wall_body, env.id, env.np_random, indices=-1)

    return wall_agent


def create_room(
    env: AssistiveEnv, sw_pos: PointXY, ne_pos: PointXY, openings: List[ROOM_OPENINGS]
):

    if not (
        (ne_pos.x - sw_pos.x) > MIN_WALL_LENGTH
        or (ne_pos.y - sw_pos.y) > MIN_WALL_LENGTH
    ):
        raise ValueError(ne_pos, sw_pos)

    # Left wall
    wall_sw_pos = PointXY(x=sw_pos.x, y=sw_pos.y)
    wall_length = ne_pos.y - sw_pos.y
    if ROOM_OPENINGS.SW_LEFT in openings:
        wall_sw_pos.y += OPENING_LENGTH
        wall_length -= OPENING_LENGTH
    if ROOM_OPENINGS.NW_LEFT in openings:
        wall_length -= OPENING_LENGTH
    create_wall(
        env, sw_pos=wall_sw_pos, wall_length=wall_length, lateral_orientation=False
    )

    # Top wall
    wall_sw_pos = PointXY(x=sw_pos.x, y=ne_pos.y)
    wall_length = ne_pos.x - sw_pos.x
    if ROOM_OPENINGS.NW_TOP in openings:
        wall_sw_pos.x += OPENING_LENGTH
        wall_length -= OPENING_LENGTH
    if ROOM_OPENINGS.NE_TOP in openings:
        wall_length -= OPENING_LENGTH
    create_wall(
        env, sw_pos=wall_sw_pos, wall_length=wall_length, lateral_orientation=True
    )

    # Right wall
    wall_sw_pos = PointXY(x=ne_pos.x - WALL_WIDTH, y=sw_pos.y)
    wall_length = ne_pos.y - sw_pos.y
    if ROOM_OPENINGS.SE_RIGHT in openings:
        wall_sw_pos.y += OPENING_LENGTH
        wall_length -= OPENING_LENGTH
    if ROOM_OPENINGS.NE_RIGHT in openings:
        wall_length -= OPENING_LENGTH
    create_wall(
        env, sw_pos=wall_sw_pos, wall_length=wall_length, lateral_orientation=False
    )

    # Bottom wall
    wall_sw_pos = PointXY(x=sw_pos.x, y=sw_pos.y)
    wall_length = ne_pos.x - sw_pos.x
    if ROOM_OPENINGS.SW_BOTTOM in openings:
        wall_sw_pos.x += OPENING_LENGTH
        wall_length -= OPENING_LENGTH
    if ROOM_OPENINGS.SE_BOTTOM in openings:
        wall_length -= OPENING_LENGTH
    create_wall(
        env, sw_pos=wall_sw_pos, wall_length=wall_length, lateral_orientation=True
    )


def setup_rooms(env: AssistiveEnv):
    for room, room_config in ROOM_CONFIGS.items():
        create_room(env, **room_config)
