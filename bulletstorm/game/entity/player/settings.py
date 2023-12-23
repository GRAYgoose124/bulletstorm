from dataclasses import dataclass

import arcade


@dataclass
class PlayerConfig(dict):
    FORWARD_ACCELERATION: float = 1
    LATERAL_ACCELERATION: float = 1
    TURN_VELOCITY: float = 0.001
    MAX_TURN_VELOCITY: float = 10.0
    DRAG: float = 0.99

    SHOOT_COOLDOWN: float = 0.5
    PROJECTILE_SPEED: float = 200


@dataclass
class PlayerKeybinds(dict):
    MOVE_FORWARD: int = arcade.key.W
    MOVE_BACKWARD: int = arcade.key.S
    TURN_LEFT: int = arcade.key.A
    TURN_RIGHT: int = arcade.key.D

    SHOOT: int = arcade.key.SPACE

    PAUSE_MENU: int = arcade.key.ESCAPE


class PlayerSettings(dict):
    def __init__(self):
        self.config = PlayerConfig()
        self.keybinds = PlayerKeybinds()
