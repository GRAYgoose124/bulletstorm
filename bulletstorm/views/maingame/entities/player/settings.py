from dataclasses import dataclass

import arcade


@dataclass
class PlayerConfig:
    FORWARD_ACCELERATION: float = 4
    LATERAL_ACCELERATION: float = 1
    TURN_VELOCITY: float = 0.05
    MAX_TURN_VELOCITY: float = 5.0
    DRAG: float = 0.9

    MAX_HP: int = 30

    SHOOT_COOLDOWN: float = 0.01
    PROJECTILE_SPEED: float = 500

    SHOCKLINE_DEPTH: int = 3

    GRAPHGROW: bool = True


def arcade_key_map(v, no_mods=True):
    for k, v2 in filter(
        lambda e: not e[0].startswith("_") and not e[0].startswith("MOD_"),
        arcade.key.__dict__.items(),
    ):
        if v == v2:
            return k


@dataclass
class PlayerKeybinds:
    MOVE_FORWARD: int = arcade.key.W
    MOVE_BACKWARD: int = arcade.key.S
    TURN_LEFT: int = arcade.key.A
    TURN_RIGHT: int = arcade.key.D

    SHOOT: int = arcade.key.SPACE
    SHOCKLINE: int = arcade.key.V
    DISCONNECT: int = arcade.key.B
    SPLIT: int = arcade.key.G
    GRAPHGROW: int = arcade.key.H

    PAUSE_MENU: int = arcade.key.ESCAPE

    def __iter__(self):
        # map control codes to their names (MOVE_FORWARD, int) -> (MOVE_FORWARD, "W")
        for control, code in filter(
            lambda e: not e[0].startswith("_"), self.__dict__.items()
        ):
            yield control, arcade_key_map(code)


class PlayerSettings(dict):
    def __init__(self):
        self.config = PlayerConfig()
        self.keybinds = PlayerKeybinds()
