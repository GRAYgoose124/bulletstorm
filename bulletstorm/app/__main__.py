import arcade

from .window import BulletStorm
from .log import setup_logging


def main():
    setup_logging()

    app = BulletStorm()

    arcade.run()


if __name__ == "__main__":
    main()
