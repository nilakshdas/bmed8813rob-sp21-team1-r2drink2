from typing import Dict, Optional, Set, Tuple, Union

import numpy as np
import pybullet as p

from assistive_gym.envs.agents.stretch import Stretch


class TeleOpRobot(object):
    TELEOP_ACTIONS_CONTROL_JOINTS: Dict[str, Tuple[Union[Tuple[int, ...], int], float]]
    TELEOP_ACTIONS_PERFORM_SPECIAL: Set[str]

    def _perform_special_action(self, action_name: str):
        raise NotImplementedError

    def get_teleop_action(
        self, action_name: str, current_action: Optional[np.ndarray] = None
    ) -> np.ndarray:

        num_joints = len(self.controllable_joint_indices)

        if current_action is None:
            action = np.zeros(num_joints)

        elif (len(current_action.shape) != 1) or (
            current_action.shape[0] != num_joints
        ):
            raise ValueError(current_action)

        else:
            action = np.copy(current_action)

        if action_name in self.TELEOP_ACTIONS_CONTROL_JOINTS.keys():
            joints, gain = self.TELEOP_ACTIONS_CONTROL_JOINTS[action_name]
            action[joints] += gain

        elif action_name in self.TELEOP_ACTIONS_PERFORM_SPECIAL:
            self._perform_special_action(action_name)

        return action


class TeleOpStretch(Stretch, TeleOpRobot):
    TELEOP_ACTIONS_CONTROL_JOINTS = dict(
        move_base_forward=([0, 1], 1.0),
        move_base_backward=([0, 1], -1.0),
        rotate_base_left=(0, 1.0),
        rotate_base_right=(1, 1.0),
        move_arm_up=(2, 1.0),
        move_arm_down=(2, -1.0),
        extend_arm_out=(3, 1.0),
        detract_arm_in=(3, -1.0),
        rotate_gripper_left=(4, 1.0),
        rotate_gripper_right=(4, -1.0),
    )

    TELEOP_ACTIONS_PERFORM_SPECIAL = {"open_gripper", "close_gripper"}

    def _perform_special_action(self, action_name: str):
        indices = self.right_gripper_indices
        forces = [500] * len(indices)
        gains = np.array([0.05] * len(indices))

        if action_name == "open_gripper":
            positions = [np.pi / 2] * len(indices)
        elif action_name == "close_gripper":
            positions = [0] * len(indices)
        else:
            raise ValueError(action_name)

        p.setJointMotorControlArray(
            self.body,
            jointIndices=indices,
            controlMode=p.POSITION_CONTROL,
            targetPositions=positions,
            positionGains=gains,
            forces=forces,
        )
