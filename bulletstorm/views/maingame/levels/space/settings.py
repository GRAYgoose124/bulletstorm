import arcade

from dataclasses import dataclass

from .....core.entity.player.settings import (
    PlayerConfig,
    PlayerKeybinds,
    PlayerSettings,
)


@dataclass
class SGPlayerConfig(PlayerConfig):
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


@dataclass
class SGPlayerKeybinds(PlayerKeybinds):
    MOVE_FORWARD: int = arcade.key.W
    MOVE_BACKWARD: int = arcade.key.S
    TURN_LEFT: int = arcade.key.A
    TURN_RIGHT: int = arcade.key.D

    SHOOT: int = arcade.key.SPACE
    SHOCKLINE: int = arcade.key.V
    DISCONNECT: int = arcade.key.B
    SPLIT: int = arcade.key.G
    GRAPHGROW: int = arcade.key.H
    GRAPHTIGHTEN: int = arcade.key.J

    PAUSE_MENU: int = arcade.key.ESCAPE


SpaceGamePlayerSettings = PlayerSettings(SGPlayerConfig(), SGPlayerKeybinds())
