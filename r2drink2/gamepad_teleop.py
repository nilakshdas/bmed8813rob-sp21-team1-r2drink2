import numpy as np
import pybullet as p

from assistive_gym.envs.env import AssistiveEnv

from r2drink2.camera import TeleOpCamera
import r2drink2.controller as controller

gamepad = controller.XboxController()
gamepad.start()

gamepad_state = gamepad.get_state()

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

class GamepadTeleOpController(TeleOpController):
    CAMERA_KEYS = {
        gamepad_state["right_stick_y_up"]: "tilt_up",
        gamepad_state["right_stick_y_down"]: "tilt_down",
        gamepad_state["right_stick_x_left"]: "pan_left",
        gamepad_state["right_stick_x_right"]: "pan_right",
        gamepad_state["start_button_pressed"]: "reset_drive_mode",
        gamepad_state["select_button_pressed"]: "reset_tool_mode",
    }

    ROBOT_KEYS = {
        gamepad_state["left_stick_y_up"]: "move_base_forward",
        gamepad_state["left_stick_y_down"]: "move_base_backward",
        gamepad_state["left_stick_x_left"]: "rotate_base_left",
        gamepad_state["left_stick_x_right"]: "rotate_base_right",
        gamepad_state["left_button_pressed"]: "move_arm_up",
        gamepad_state["top_button_pressed"]: "move_arm_down",
        gamepad_state["right_trigger_pulled"]: "extend_arm_out",
        gamepad_state["left_trigger_pulled"]: "detract_arm_in",
        gamepad_state["left_shoulder_button_pressed"]: "rotate_gripper_left",
        gamepad_state["right_shoulder_button_pressed"]: "rotate_gripper_right",
        gamepad_state["bottom_button_pressed"]: "open_gripper",
        gamepad_state["right_button_pressed"]: "close_gripper",
    }

    def _get_input_keys(self):
        input_keys = gamepad.get_state()
        print(gamepad_state)
        return input_keys

    def _get_robot_action(self, input_keys: dict) -> np.ndarray:
        action = self.env.robot.get_teleop_action(action_name=None)
        
        for key, action_name in self.ROBOT_KEYS.items():
            # print(key, action_name)
            if key in input_keys and input_keys[key]:
                action = self.env.robot.get_teleop_action(
                    action_name=action_name, current_action=action
                )

        return action

    def _update_camera_view(self, input_keys: dict):
        for gamepad_state, teleop_fn_name in self.CAMERA_KEYS.items():
            if gamepad_state in input_keys and gamepad_state:
                teleop_fn = getattr(self.teleop_camera, teleop_fn_name)
                teleop_fn()

        self.teleop_camera.update_env_camera()