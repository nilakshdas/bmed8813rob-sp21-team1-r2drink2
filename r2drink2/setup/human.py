import numpy as np

import assistive_gym.envs.agents.human as h
from assistive_gym.envs.env import AssistiveEnv


def setup_human(env: AssistiveEnv):
    human = env.create_human(
        controllable=False,
        controllable_joint_indices=h.right_arm_joints,
        fixed_base=False,
        human_impairment="none",
        gender="random",
        mass=None,
        radius_scale=1.0,
        height_scale=1.0,
    )

    # Define the initial pose for the human
    joints_positions = [
        (human.j_right_elbow, -90),
        (human.j_left_elbow, -90),
        (human.j_right_hip_x, -80),
        (human.j_right_knee, 80),
        (human.j_left_hip_x, -80),
        (human.j_left_knee, 80),
    ]
    human.setup_joints(
        joints_positions,
        use_static_joints=False,
        reactive_force=None,
        reactive_gain=0.05,
    )

    # Set human on chair and increase body friction
    chair = env.furniture
    chair_pos, chair_orient = chair.get_base_pos_orient()
    human.set_base_pos_orient(
        chair_pos
        + np.array([0.01, 0, -0.5 + (0.89 if human.gender == "male" else 0.86)]),
        env.get_quaternion(env.get_euler(chair_orient) + np.array([-0.1, 0, 0])),
    )
    human.set_whole_body_frictions(
        lateral_friction=10, spinning_friction=10, rolling_friction=10
    )
    # Stiffen the joints so they do not fall limp so easily
    human.set_all_joints_stiffness(0.01)
