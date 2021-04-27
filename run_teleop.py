import argparse

from r2drink2.env import R2Drink2Env
from r2drink2.teleop import GamepadTeleOpController, KeyboardTeleOpController


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--seed", type=int, default=42)
    parser.add_argument("-g", "--gamepad", action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    env = R2Drink2Env(render=True, seed=args.seed)

    teleop_controller = (
        GamepadTeleOpController(env) if args.gamepad else KeyboardTeleOpController(env)
    )

    while True:
        teleop_controller.take_step()
        env.render()


if __name__ == "__main__":
    main()
