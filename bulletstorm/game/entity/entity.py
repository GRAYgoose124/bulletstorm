import arcade


class Entity(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set by the entity manager
        self.body = None
        self.manager = None

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        return True

    def update(self, delta_time):
        pass