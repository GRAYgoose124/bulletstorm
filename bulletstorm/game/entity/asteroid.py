from .core.base import Entity
from ...app.log import setup_logging

log = setup_logging(__name__)


class Asteroid(Entity):
    def collision_handler(self, entity_a, entity_b, arbiter, space, data):
        # log.debug("collision between %s and %s", entity_a, entity_b)
        # damage player
        if any([entity_a.tag == "player", entity_b.tag == "player"]):
            print("collision between %s and %s" % (entity_a, entity_b))
        if entity_b.tag == "player":
            target = entity_b
        elif entity_a.tag == "player":
            target = entity_a
        else:
            target = None

        if target is not None:
            target.take_damage(1, cooldown=0.25)

        # if either entity has a line, connect a new one with manager - shockline op todo: upgrade for it
        if entity_a.tag == "asteroid" and entity_b.tag == "asteroid":
            if self.manager.has_line(entity_a) or self.manager.has_line(entity_b):
                self.manager.add_line_between(entity_a, entity_b)

        return True
