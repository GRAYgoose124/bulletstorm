from dataclasses import dataclass

import arcade


@dataclass
class PlayerConfig(dict):
    FORWARD_ACCELERATION: float = 4
    LATERAL_ACCELERATION: float = 1
    TURN_VELOCITY: float = 0.33
    MAX_TURN_VELOCITY: float = 5.0
    DRAG: float = 0.9

    SHOOT_COOLDOWN: float = 0.5
    PROJECTILE_SPEED: float = 500


@dataclass
class PlayerKeybinds(dict):
    MOVE_FORWARD: int = arcade.key.W
    MOVE_BACKWARD: int = arcade.key.S
    TURN_LEFT: int = arcade.key.A
    TURN_RIGHT: int = arcade.key.D

    SHOOT: int = arcade.key.SPACE
    SHOCKLINE: int = arcade.key.V

    PAUSE_MENU: int = arcade.key.ESCAPE


class PlayerSettings(dict):
    def __init__(self):
        self.config = PlayerConfig()
        self.keybinds = PlayerKeybinds()
