from typing import Optional

import numpy as np

from assistive_gym.envs.agents.stretch import Stretch


class TeleOpStretch(Stretch):
    TELEOP_ACTIONS = dict(
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

        if action_name in self.TELEOP_ACTIONS.keys():
            joints, gain = self.TELEOP_ACTIONS[action_name]
            action[joints] += gain

        return action
