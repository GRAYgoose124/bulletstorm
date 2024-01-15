from ...utils import setup_logging
from ...entity.base import Entity


log = setup_logging(__name__)


class Player(Entity):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings = settings
        self.hp = self.gameplay_settings.MAX_HP

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

        self.angular_acc *= self.gameplay_settings.DRAG
        body.angular_velocity *= self.gameplay_settings.DRAG
        self.manager.apply_impulse(self, self.acceleration)

    def post_solve(self, entity_a, entity_b, arbiter, space, data):
        pass

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        if sprite_b is not None and sprite_a is not None:
            self.take_damage(1, cooldown=0)
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

    def reset(self):
        self.angle = 0
        self.acceleration = [0, 0]
        self.change_angle = 0
        self.angular_acc = 0
        self.hp = self.gameplay_settings.MAX_HP
        self.is_firing = False
