import numpy as np
import pybullet as p
from numpngw import write_apng

from assistive_gym.envs.env import AssistiveEnv


from r2drink2.setup.chair import setup_chair
from r2drink2.setup.human import setup_human
from r2drink2.setup.misc import setup_plane
from r2drink2.setup.robot import setup_robot


def create_env():
    env = AssistiveEnv()
    env.set_seed(200)

    env.setup_camera(
        camera_eye=[1.75, -1.5, 2],
        camera_target=[-0.6, -0.25, 0.4],
        camera_width=1920 // 4,
        camera_height=1080 // 4,
        fov=60,
    )

    env.reset()

    setup_plane(env)
    setup_chair(env)
    setup_human(env)
    setup_robot(env)

    return env


def update_camera(env: AssistiveEnv):
    robot_pos, _ = env.robot.get_base_pos_orient()

    camera_eye = np.copy(robot_pos)
    camera_eye[:2] += 0.5  # x and y axes
    camera_eye[2] += 0.8  # z-axis

    camera_target = np.copy(robot_pos)
    camera_target[:2] += 0.4  # x and y axes
    camera_target[2] = 0  # z-axis

    env.setup_camera(
        camera_eye,
        camera_target,
        camera_width=1920 // 4,
        camera_height=1080 // 4,
        fov=60,
    )


def render_env(num_frames=10):
    env = create_env()
    update_camera(env)

    frames = []
    done = False
    for _ in range(num_frames):
        action = np.zeros(len(env.robot.controllable_joint_indices))
        action[: len(env.robot.wheel_joint_indices) + 1] = 1.0
        env.take_step(action)
        update_camera(env)
        img, depth = env.get_camera_image_depth()
        frames.append(img)
    env.disconnect()

    return frames


def main():
    frames = render_env()
    write_apng("output.png", np.uint8(frames), delay=100)


if __name__ == "__main__":
    main()
