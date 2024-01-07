import arcade

from bulletstorm.window import BulletStorm
from bulletstorm.log import setup_logging


def main():
    setup_logging()

    app = BulletStorm()

    arcade.run()


if __name__ == "__main__":
    main()
