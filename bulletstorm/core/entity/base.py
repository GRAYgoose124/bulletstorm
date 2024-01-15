import time
import arcade


class Entity(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        # pop hp
        hp = kwargs.pop("hp", 5)
        super().__init__(*args, **kwargs)
        # set by the entity manager
        self.body = None
        self.manager = None

        # game data
        self.hp = hp
        self.cooldown = 0
        self.is_firing = False

        # physics data
        self.acceleration = [0, 0]
        self.angular_acc = 0

    def reset(self):
        self.hp = 5
        self.cooldown = None

        self.acceleration = [0, 0]
        self.angular_acc = 0

        self.is_firing = False

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        return True

    def post_solve(self, arbiter, space, data):
        pass

    def update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time
            if self.cooldown <= 0:
                self.cooldown = 0

        super().update()

    def take_damage(self, damage=1, cooldown=1.0):
        if self.cooldown <= 0 or cooldown <= 0:
            self.hp -= damage
            self.cooldown += cooldown
