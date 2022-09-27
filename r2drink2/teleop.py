import numpy as np
import pybullet as p

try:
    from stretch_body.xbox_controller import XboxController
except ImportError:
    print("WARNING: Gamepad controller will not work.")

from assistive_gym.envs.env import AssistiveEnv

from r2drink2.camera import TeleOpCamera

KEYBOARD_CODES = dict(UP=65297, DOWN=65298, LEFT=65295, RIGHT=65296)


class TeleOpController:
    def __init__(self, env: AssistiveEnv, free_view: bool = False):
        self.env = env
        self.teleop_camera = TeleOpCamera(env)

        self._free_view = free_view

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

        if not self._free_view:
            self._update_camera_view(input_keys)


class KeyboardTeleOpController(TeleOpController):
    CAMERA_KEYS = {
        ord("e"): "tilt_up",
        ord("r"): "tilt_down",
        ord("d"): "pan_left",
        ord("f"): "pan_right",
        ord("q"): "reset_drive_mode",
        ord("a"): "reset_tool_mode",
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
        ord("h"): "open_gripper",
        ord("j"): "close_gripper",
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


class GamepadTeleOpController(TeleOpController):
    CAMERA_KEYS = {
        "right_stick_y_up": "tilt_up",
        "right_stick_y_down": "tilt_down",
        "right_stick_x_left": "pan_left",
        "right_stick_x_right": "pan_right",
        "start_button_pressed": "reset_drive_mode",
        "select_button_pressed": "reset_tool_mode",
    }

    ROBOT_KEYS = {
        "left_stick_y_up": "move_base_forward",
        "left_stick_y_down": "move_base_backward",
        "left_stick_x_left": "rotate_base_left",
        "left_stick_x_right": "rotate_base_right",
        "top_pad_pressed": "move_base_forward",
        "bottom_pad_pressed": "move_base_backward",
        "left_pad_pressed": "rotate_base_left",
        "right_pad_pressed": "rotate_base_right",
        "left_button_pressed": "move_arm_up",
        "top_button_pressed": "move_arm_down",
        "right_trigger_pulled": "extend_arm_out",
        "left_trigger_pulled": "detract_arm_in",
        "left_shoulder_button_pressed": "rotate_gripper_left",
        "right_shoulder_button_pressed": "rotate_gripper_right",
        "bottom_button_pressed": "open_gripper",
        "right_button_pressed": "close_gripper",
    }

    def __init__(self, env: AssistiveEnv, free_view: bool = False):
        super().__init__(env, free_view=free_view)
        self.gamepad = XboxController()
        self.gamepad.start()

    def _get_updated_gamepad_state(self) -> dict:
        deadzone_sensitivity = 0.4
        trigger_sensitivity = 0.5

        def _get_stick_boolean_state(analog_value: float, is_positive: bool) -> bool:
            sens = deadzone_sensitivity
            sens *= 1 if is_positive else -1
            if is_positive:
                return analog_value >= sens
            else:
                return analog_value <= sens

        state = self.gamepad.get_state()

        # analog_keys = [
        #     "left_stick_x",
        #     "left_stick_y",
        #     "right_stick_x",
        #     "right_stick_y",
        # ]
        # for analog_key in analog_keys:
        #     if analog_key.endswith("_x"):
        #         state[f"{analog_key}_right"] = _get_stick_boolean_state(state[analog_key], is_positive=True)
        #         state[f"{analog_key}_left"] = _get_stick_boolean_state(state[analog_key], is_positive=False)
        #     elif analog_key.endswith("_y"):
        #         state[f"{analog_key}_up"] = _get_stick_boolean_state(state[analog_key], is_positive=True)
        #         state[f"{analog_key}_down"] = _get_stick_boolean_state(state[analog_key], is_positive=False)

        # right_stick_y_up
        state["right_stick_y_up"] = _get_stick_boolean_state(
            state["right_stick_y"], is_positive=False
        )

        # right_stick_y_down
        state["right_stick_y_down"] = _get_stick_boolean_state(
            state["right_stick_y"], is_positive=True
        )

        # right_stick_x_left
        state["right_stick_x_left"] = _get_stick_boolean_state(
            state["right_stick_x"], is_positive=False
        )

        # right_stick_x_right
        state["right_stick_x_right"] = _get_stick_boolean_state(
            state["right_stick_x"], is_positive=True
        )

        # left_stick_y_up
        state["left_stick_y_up"] = _get_stick_boolean_state(
            state["left_stick_y"], is_positive=False
        )

        # left_stick_y_down
        state["left_stick_y_down"] = _get_stick_boolean_state(
            state["left_stick_y"], is_positive=True
        )

        # left_stick_x_left
        state["left_stick_x_left"] = _get_stick_boolean_state(
            state["left_stick_x"], is_positive=False
        )

        # left_stick_x_right
        state["left_stick_x_right"] = _get_stick_boolean_state(
            state["left_stick_x"], is_positive=True
        )

        # right_trigger_pulled
        state["right_trigger_pulled"] = (
            state["right_trigger_pulled"] >= trigger_sensitivity
        )

        # left_trigger_pulled
        state["left_trigger_pulled"] = (
            state["left_trigger_pulled"] >= trigger_sensitivity
        )

        return state

    def _get_input_keys(self):
        input_keys = self._get_updated_gamepad_state()
        # print(f"{input_keys}\n---")
        return input_keys

    def _get_robot_action(self, state: dict) -> np.ndarray:
        action = self.env.robot.get_teleop_action(action_name=None)

        for key, action_name in self.ROBOT_KEYS.items():
            if state[key] is True:
                action = self.env.robot.get_teleop_action(
                    action_name=action_name, current_action=action
                )

        return action

    def _update_camera_view(self, state: dict):
        for key, teleop_fn_name in self.CAMERA_KEYS.items():
            if state[key] is True:
                teleop_fn = getattr(self.teleop_camera, teleop_fn_name)
                teleop_fn()

        self.teleop_camera.update_env_camera()
