from pymunk import Vec2d
from ..entity.core.base import Entity
from ....log import setup_logging

log = setup_logging(__name__)


class Asteroid(Entity):
    def collision_handler(self, entity_a, entity_b, arbiter, space, data):
        # log.debug("collision between %s and %s", entity_a, entity_b)
        # damage player
        # if any([entity_a.tag == "player", entity_b.tag == "player"]):
        #     print("collision between %s and %s" % (entity_a, entity_b))
        # if entity_b.tag == "player":
        #     target = entity_b
        # elif entity_a.tag == "player":
        #     target = entity_a
        # else:
        #     target = None

        # if target is not None:
        #     impact_vel = arbiter.total_impulse.length
        #     target.take_damage(10 * impact_vel, cooldown=0)

        # if either entity has a line, connect a new one with manager - shockline op todo: upgrade for it
        if entity_a.tag == "asteroid" and entity_b.tag == "asteroid":
            if (
                self.manager.has_line(entity_a) or self.manager.has_line(entity_b)
            ) and (
                (
                    entity_a in self.manager.entity_graph
                    and self.manager.entity_graph.degree(entity_a) < 5
                    or entity_a not in self.manager.entity_graph
                )
                and (
                    entity_b in self.manager.entity_graph
                    and self.manager.entity_graph.degree(entity_b) < 5
                    or entity_b not in self.manager.entity_graph
                )
            ):
                self.manager.add_line_between(entity_a, entity_b)

        return True
