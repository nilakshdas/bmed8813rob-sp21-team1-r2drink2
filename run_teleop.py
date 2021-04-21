from r2drink2.env import R2Drink2Env
from r2drink2.teleop import KeyboardTeleOpController


def main():
    env = R2Drink2Env(render=True)
    teleop_controller = KeyboardTeleOpController(env)

    while True:
        teleop_controller.take_step()
        env.render()


if __name__ == "__main__":
    main()
