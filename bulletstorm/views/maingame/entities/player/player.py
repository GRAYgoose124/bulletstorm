from .....core.entity.player import Player
from .....core.utils import setup_logging

from ..asteroid import Asteroid
from .attacks import shoot, shockline

log = setup_logging(__name__)


class SpacePlayer(Player):
    def post_solve(self, entity_a, entity_b, arbiter, space, data):
        Asteroid.post_solve(self, entity_a, entity_b, arbiter, space, data)

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):
        if sprite_b is not None and sprite_a is not None:
            self.take_damage(1, cooldown=0)
        return True

    def key_handler(self, key, modifiers, release=False):
        super().key_handler(key, modifiers, release)
        if key == self.keybinds.SHOOT:
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
