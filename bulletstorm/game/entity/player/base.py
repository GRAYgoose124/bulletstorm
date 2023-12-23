from dataclasses import dataclass
import time
import arcade

from bulletstorm.game.entity import Entity
from bulletstorm.game.entity.projectile import Projectile
from bulletstorm.game.entity.player.settings import PlayerSettings


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprite = None

        self.hp = 100
        self.last_hit = None

        self.acceleration = [0, 0]
        self.angular_acc = 0

        self.is_firing = False

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

    def reset(self):
        self.hp = 100
        self.last_hit = None

        self.acceleration = [0, 0]
        self.angular_acc = 0

        self.is_firing = False

    def update(self, delta_time):
        body = self.manager.get_physics_object(self).body
        if self.change_angle != 0:
            self.angular_acc += self.change_angle / (1 + abs(self.angular_acc))
            body.angular_velocity += self.angular_acc

            if abs(body.angular_velocity) > self.gameplay_settings.MAX_TURN_VELOCITY:
                body.angular_velocity = self.gameplay_settings.MAX_TURN_VELOCITY * (
                    body.angular_velocity / abs(body.angular_velocity)
                )

        self.angular_acc *= 0.99
        body.angular_velocity *= 0.99
        self.manager.apply_impulse(self, self.acceleration)

    def take_damage(self, damage=1, cooldown=1.0):
        t = time.time()
        if self.last_hit is None or t - self.last_hit > cooldown:
            self.hp -= damage
            self.last_hit = t

    def shoot(self):
        x, y = self.center_x, self.center_y
        projectile = Projectile(
            center_x=self.center_x, center_y=self.center_y, angle=self.angle + 90
        )
        self.manager.add_entity(
            projectile,
            collision_type="projectile",
            collision_type_b="enemy",
            tag="projectile",
        )
        self.manager.apply_impulse(
            projectile, [self.gameplay_settings.PROJECTILE_SPEED, 0]
        )

        # make projectile frictionless
        proj = self.manager.get_physics_object(projectile)
        proj.body.friction = 0

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        self.take_damage(10)
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
            self.shoot()
