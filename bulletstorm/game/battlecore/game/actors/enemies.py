from ...core import Actor, ActorStats
from ..actions.attacks import slash_attack


class Enemy(Actor):
    pass


skeleton_enemy = lambda: Enemy(
    "Skeleton",
    actions=[
        slash_attack,
    ],
    statistics=ActorStats(health=5, stamina=5, mana=5, dexterity=3),
)


__all__ = [
    "skeleton_enemy",
]
