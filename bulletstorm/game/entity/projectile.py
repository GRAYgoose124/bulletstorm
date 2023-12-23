from .core.base import Entity


class Projectile(Entity):
    def __init__(self, origin, *args, **kwargs):
        self.origin = origin
        resource = ":resources:images/space_shooter/laserBlue01.png"
        super().__init__(resource, *args, **kwargs)

    def collision_handler(self, entity_a, entity_b, arbiter, space, data):
        self.manager.remove_entity(entity_a)

        # damage sprite_b
        entity_b.hp -= 1

        # add line from origin to sprite_b
        self.manager.add_line_between(self.origin, entity_b)
        return False
