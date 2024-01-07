from ...entity.base import Entity

from .settings import PlayerSettings
from .attacks import shoot, shockline


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings = PlayerSettings()
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

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        if sprite_b is not None and sprite_a is not None:
            # do self damage if we hit an asteroid
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
        # actions
        elif key == self.keybinds.SHOOT:
            # self.is_firing = not release
            if not release:
                shoot(self, target_tag="enemy")
        elif key == self.keybinds.SHOCKLINE:
            if not release:
                shockline(self)
        elif key == self.keybinds.DISCONNECT:
            if not release:
                # disconnect one line from the player
                if self.manager.has_line(self):
                    neighbors = self.manager.entity_graph.adj[self]
                    if neighbors:
                        self.manager.remove_line_from(self, next(iter(neighbors)))
                        self.manager.remove_entity_from_graph(self)
        elif key == self.keybinds.SPLIT:
            if not release:
                # follow the lines from the player and split from the first node that is not the player
                if self.manager.has_line(self):
                    neighbors = self.manager.entity_graph.adj[self]
                    if neighbors:
                        for n in list(neighbors):
                            self.manager.remove_entity_from_graph(n)
                    self.manager.remove_entity_from_graph(self)
        elif key == self.keybinds.GRAPHGROW:
            if release:
                self.gameplay_settings.GRAPHGROW = not self.gameplay_settings.GRAPHGROW

    def reset(self):
        self.angle = 0
        self.acceleration = [0, 0]
        self.change_angle = 0
        self.angular_acc = 0
        self.hp = self.gameplay_settings.MAX_HP
        self.is_firing = False
