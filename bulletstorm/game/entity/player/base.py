from dataclasses import dataclass
import time
import arcade

from ...entity import Entity
from ...entity.projectile import Projectile
from .settings import PlayerSettings
from ..actions.attacks import shoot, shockline


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings = PlayerSettings()

    @property
    def settings(self):
        return self._settings

    @property
    def gameplay_settings(self):
        return self._settings.config

    @property
    def keybinds(self):
        return self._settings.keybinds

    def update(self, delta_time):
        body = self.manager.get_physics_object(self).body
        if (
            self.change_angle != 0
            or body.angular_velocity != 0
            or self.acceleration != [0, 0]
        ):
            self.angular_acc += self.change_angle / (1 + abs(self.angular_acc))
            body.angular_velocity += self.angular_acc

            if abs(body.angular_velocity) > self.gameplay_settings.MAX_TURN_VELOCITY:
                body.angular_velocity = self.gameplay_settings.MAX_TURN_VELOCITY * (
                    body.angular_velocity / abs(body.angular_velocity)
                )

        self.angular_acc *= 0.99
        body.angular_velocity *= 0.99
        self.manager.apply_impulse(self, self.acceleration)

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        return True

    def key_handler(self, key, modifiers, release=False):
        if key == self.keybinds.MOVE_FORWARD:
            self.acceleration[1] = (
                0 if release else self.gameplay_settings.FORWARD_ACCELERATION
            )
        elif key == self.keybinds.MOVE_BACKWARD:
            self.acceleration[1] = (
                0 if release else -self.gameplay_settings.FORWARD_ACCELERATION
            )
        elif key == self.keybinds.TURN_LEFT:
            self.change_angle = 0 if release else self.gameplay_settings.TURN_VELOCITY
        elif key == self.keybinds.TURN_RIGHT:
            self.change_angle = 0 if release else -self.gameplay_settings.TURN_VELOCITY
        elif key == self.keybinds.SHOOT:
            # self.is_firing = not release
            if not release:
                shoot(self, target_tag="enemy")
        elif key == self.keybinds.SHOCKLINE:
            if not release:
                shockline(self)
