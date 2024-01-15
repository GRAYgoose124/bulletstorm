import arcade

from .window import BulletStorm
from .core.utils import setup_logging


def main():
    setup_logging(__name__)

    app = BulletStorm()

    arcade.run()


if __name__ == "__main__":
    main()
