import numpy as np
import pybullet as p
from numpngw import write_apng

from assistive_gym.envs.env import AssistiveEnv

from r2drink2.camera import TeleOpCamera
from r2drink2.setup.chair import setup_chair
from r2drink2.setup.human import setup_human
from r2drink2.setup.misc import setup_plane
from r2drink2.setup.robot import setup_robot


OVERHEAD_CAMERA_KWARGS = dict(
    camera_eye=[1.75, -1.5, 2],
    camera_target=[-0.6, -0.25, 0.4],
    camera_width=1920 // 4,
    camera_height=1080 // 4,
    fov=60,
)


class R2Drink2Env(AssistiveEnv):
    def __init__(self, render=False, seed=42):
        super().__init__(render=render, seed=seed)

        self.set_seed(seed)
        self.reset()

        setup_plane(self)
        setup_chair(self)
        #  setup_human(self)
        setup_robot(self)

        self.setup_camera(**OVERHEAD_CAMERA_KWARGS)


def render_env_static(num_frames=100):
    env = R2Drink2Env()
    teleop_camera = TeleOpCamera(env)

    frames = []
    for _ in range(num_frames):
        action = env.robot.get_teleop_action(None)
        env.take_step(action)
        teleop_camera.pan_left()
        frames.append(teleop_camera.update_camera_and_get_frame())
        #  teleop_camera.tilt_down()
        #  frames.append(teleop_camera.get_frame())

    env.disconnect()

    return frames


def main():
    frames = render_env_static()
    write_apng("output.png", frames, delay=100)


if __name__ == "__main__":
    main()
