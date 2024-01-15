from ..entity.base import Entity
from ....log import setup_logging

log = setup_logging(__name__)


class Asteroid(Entity):
    def post_solve(self, entity_a, entity_b, arbiter, space, data):
        if any([entity_a.tag == "player", entity_b.tag == "player"]):
            print("collision between %s and %s" % (entity_a, entity_b))
            target = entity_a.manager.parent.player
        else:
            return True

        impact_vel = arbiter.total_impulse.length
        if impact_vel > 0:
            target.take_damage(10 * impact_vel, cooldown=0)
            log.debug("asteroid hit player for %s damage", 10 * impact_vel)

    def collision_handler(self, entity_a, entity_b, arbiter, space, data):
        # log.debug("collision between %s and %s", entity_a, entity_b)
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
                if (
                    self.manager.parent.player in self.manager.entity_graph
                    and self.manager.parent.player.gameplay_settings.GRAPHGROW
                ):
                    self.manager.add_line_between(entity_a, entity_b)

        return True
