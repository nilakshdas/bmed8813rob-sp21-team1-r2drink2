from assistive_gym.envs.agents.stretch import Stretch


class CustomStretch(Stretch):
    def __init__(self):
        super().__init__(controllable_joints="wheel_right")
