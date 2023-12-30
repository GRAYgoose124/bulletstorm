from ..entity.base import Entity


# TODO: should be a particle, follow explosion's lead.
class Projectile(Entity):
    def __init__(self, origin, *args, **kwargs):
        self.origin = origin
        resource = ":resources:images/space_shooter/laserBlue01.png"
        super().__init__(resource, *args, **kwargs)

    def collision_handler(self, entity_a, entity_b, arbiter, space, data):
        self.manager.remove_entity(entity_a)

        # damage sprite_b
        if self.origin.tag == "player" and (
            entity_b.tag == "agent" or entity_b.tag == "asteroid"
        ):
            entity_b.take_damage(5)

            # add line from origin to sprite_b
            self.manager.add_line_between(self.origin, entity_b)

        return True
