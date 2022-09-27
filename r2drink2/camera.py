import pybullet as p
import numpy as np
from scipy.spatial.transform import Rotation as R

from assistive_gym.envs.env import AssistiveEnv


def _make_unit_vector(v: np.ndarray) -> np.ndarray:
    assert len(v.shape) == 1
    return v / np.linalg.norm(v)


class TeleOpCamera:
    def __init__(self, env: AssistiveEnv):
        self.env = env

        self._tilt_unit = 0
        self._tilt_gain = 2

        self._pan_unit = 0
        self._pan_gain = 2

    @property
    def _tilt_value(self):
        return self._tilt_unit * self._tilt_gain

    @property
    def _pan_value(self):
        return self._pan_unit * self._pan_gain

    @property
    def _camera_kwargs(self):
        robot = self.env.robot
        robot_pos, robot_orient = robot.get_base_pos_orient()

        # compute correct heading for camera
        rotation1 = R.from_quat(robot_orient)
        rotation2 = R.from_rotvec(-(np.pi / 4) * np.array([0, 0, 1]))
        robot_heading = _make_unit_vector(np.ones_like(robot_pos))
        robot_heading = rotation1.apply(robot_heading)
        robot_heading = rotation2.apply(robot_heading)

        # project onto xy-plane
        robot_heading[2] = 0
        robot_heading = _make_unit_vector(robot_heading)

        # initialize camera eye
        camera_height = 1.25
        camera_eye = robot_pos + (0.5 * robot_heading)
        camera_eye[2] += camera_height

        camera_heading = np.copy(robot_heading)

        # calculate yaw
        dot_x = np.dot(robot_heading, np.array([1, 0, 0]))
        dot_y = np.dot(robot_heading, np.array([0, 1, 0]))
        yaw = np.degrees(np.arccos(dot_y))
        yaw *= -1 if dot_x > 0 else 1
        yaw += self._pan_value

        # pan camera_heading
        pan_axis = np.array([0, 0, 1])
        pan_rotation = R.from_rotvec(np.radians(self._pan_value) * pan_axis)
        camera_heading = pan_rotation.apply(camera_heading)

        # tilt camera heading
        pitch = self._tilt_value
        tilt_axis = np.cross(camera_heading, np.array([0, 0, 1]))
        tilt_rotation = R.from_rotvec(np.radians(pitch) * tilt_axis)
        camera_heading = tilt_rotation.apply(camera_heading)

        return dict(
            cameraDistance=1.0,
            cameraYaw=yaw,
            cameraPitch=pitch,
            cameraTargetPosition=camera_eye + camera_heading,
        )

    def _tilt_camera(self, num_units: float):
        self._tilt_unit += num_units

        tilt_value = self._tilt_value
        tilt_limit = 90
        if tilt_value <= -tilt_limit or tilt_value >= tilt_limit:
            self._tilt_unit -= num_units

    def _pan_camera(self, num_units: float):
        self._pan_unit += num_units

        pan_value = self._pan_value
        pan_limit = 90
        if pan_value <= -pan_limit or pan_value >= pan_limit:
            self._pan_unit -= num_units

    def tilt_up(self):
        self._tilt_camera(num_units=1)

    def tilt_down(self):
        self._tilt_camera(num_units=-1)

    def pan_left(self):
        self._pan_camera(num_units=1)

    def pan_right(self):
        self._pan_camera(num_units=-1)

    def reset_drive_mode(self):
        self._tilt_unit = 0
        self._pan_unit = 0

    def reset_tool_mode(self):
        self._tilt_unit = -4
        self._pan_unit = -44

    def update_env_camera(self) -> dict:
        camera_kwargs = self._camera_kwargs
        p.resetDebugVisualizerCamera(**camera_kwargs)
        return camera_kwargs
