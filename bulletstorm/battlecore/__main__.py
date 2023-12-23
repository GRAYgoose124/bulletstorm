import logging

from .core import *
from .game.actors.heroes import *
from .game.actors.enemies import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    player_party = Party("Player")
    player_party.add_actor(mitochondra_hero)

    enemy_party = Party("Enemy")
    enemy_party.add_actor(skeleton_enemy)

    B = Battle()
    B.add_party(player_party)
    B.add_party(enemy_party)
    BE = BattleEngine(B)
    BE.start()
