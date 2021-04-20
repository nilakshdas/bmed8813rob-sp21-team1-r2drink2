import numpy as np
import pybullet as p

from assistive_gym.envs.env import AssistiveEnv

from r2drink2.camera import TeleOpCamera

KEYBOARD_CODES = dict(UP=65297, DOWN=65298, LEFT=65295, RIGHT=65296)


class TeleOpController:
    def __init__(self, env: AssistiveEnv):
        self.env = env
        self.teleop_camera = TeleOpCamera(env)

    def _get_input_keys(self) -> dict:
        raise NotImplementedError

    def _get_robot_action(self, input_keys: dict) -> np.ndarray:
        raise NotImplementedError

    def _update_camera_view(self, input_keys: dict):
        raise NotImplementedError

    def take_step(self):
        input_keys = self._get_input_keys()
        action = self._get_robot_action(input_keys)
        self.env.take_step(action)
        self._update_camera_view(input_keys)


class KeyboardTeleOpController(TeleOpController):
    CAMERA_KEYS = {
        ord("v"): "tilt_up",
        ord("b"): "tilt_down",
        ord("n"): "pan_left",
        ord("m"): "pan_right",
    }

    ROBOT_KEYS = {
        KEYBOARD_CODES["UP"]: "move_base_forward",
        KEYBOARD_CODES["DOWN"]: "move_base_backward",
        KEYBOARD_CODES["LEFT"]: "rotate_base_left",
        KEYBOARD_CODES["RIGHT"]: "rotate_base_right",
        ord("u"): "move_arm_up",
        ord("i"): "move_arm_down",
        ord("o"): "extend_arm_out",
        ord("p"): "detract_arm_in",
        ord("k"): "rotate_gripper_left",
        ord("l"): "rotate_gripper_right",
    }

    def _get_input_keys(self):
        input_keys = p.getKeyboardEvents(self.env.id)
        return input_keys

    def _get_robot_action(self, input_keys: dict) -> np.ndarray:
        action = self.env.robot.get_teleop_action(action_name=None)

        for key, action_name in self.ROBOT_KEYS.items():
            if key in input_keys and input_keys[key] & p.KEY_IS_DOWN:
                action = self.env.robot.get_teleop_action(
                    action_name=action_name, current_action=action
                )

        return action

    def _update_camera_view(self, input_keys: dict):
        for key, teleop_fn_name in self.CAMERA_KEYS.items():
            if key in input_keys and input_keys[key] & p.KEY_IS_DOWN:
                teleop_fn = getattr(self.teleop_camera, teleop_fn_name)
                teleop_fn()

        self.teleop_camera.update_env_camera()
