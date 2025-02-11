from ...core import Enemy, ActorStats
from ..actions.attacks import slash_attack


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
