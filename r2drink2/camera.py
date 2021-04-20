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
        self._tilt_gain = np.pi / 90

        self._pan_unit = 0
        self._pan_gain = np.pi / 90

    @property
    def _tilt_value(self):
        return self._tilt_unit * self._tilt_gain

    @property
    def _pan_value(self):
        return self._pan_unit * self._pan_gain

    @property
    def camera_kwargs(self):
        robot = self.env.robot
        robot_pos, robot_orient = robot.get_base_pos_orient()

        # compute correct heading for camera
        rotation1 = R.from_quat(robot_orient)
        rotation2 = R.from_rotvec(-(np.pi / 4) * np.array([0, 0, 1]))
        unit_vec = _make_unit_vector(np.ones_like(robot_pos))
        unit_vec = rotation1.apply(unit_vec)
        unit_vec = rotation2.apply(unit_vec)

        # initialize camera eye
        camera_height = 0.75
        camera_eye = robot_pos - (0.5 * unit_vec)
        camera_eye[2] += camera_height

        # project onto xy-plane
        unit_vec[2] = 0
        unit_vec = _make_unit_vector(unit_vec)

        # add tilt
        tilt_axis = np.cross(unit_vec, np.array([0, 0, 1]))
        tilt_rotation = R.from_rotvec(self._tilt_value * tilt_axis)
        unit_vec = tilt_rotation.apply(unit_vec)

        # add pan
        pan_axis = np.array([0, 0, 1])
        pan_rotation = R.from_rotvec(self._pan_value * pan_axis)
        unit_vec = pan_rotation.apply(unit_vec)

        # initialize camera target
        camera_target = camera_eye + unit_vec

        return dict(
            camera_eye=camera_eye,
            camera_target=camera_target,
            camera_width=1920 // 4,
            camera_height=1080 // 4,
            fov=60,
        )

    def _tilt_camera(self, num_units: float):
        self._tilt_unit += num_units

        tilt_value = self._tilt_value
        tilt_limit = np.pi / 2
        if tilt_value <= -tilt_limit or tilt_value >= tilt_limit:
            self._tilt_unit -= num_units

    def _pan_camera(self, num_units: float):
        self._pan_unit += num_units

        pan_value = self._pan_value
        pan_limit = np.pi / 2
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

    def update_env_camera(self) -> dict:
        camera_kwargs = self.camera_kwargs
        self.env.setup_camera(**camera_kwargs)
        return camera_kwargs

    def get_frame(self) -> np.uint8:
        frame, depth = self.env.get_camera_image_depth()
        return np.uint8(frame)

    def update_camera_and_get_frame(self) -> np.uint8:
        self.update_env_camera()
        return self.get_frame()
