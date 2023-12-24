from ...core import Actor, ActorStats
from ..actions.attacks import slash_attack


class Hero(Actor):
    pass


mitochondra_hero = lambda: Hero(
    "Mitochondra",
    actions=[
        slash_attack,
    ],
    statistics=ActorStats(health=15, stamina=12, mana=5, dexterity=5),
)


__all__ = [
    "mitochondra_hero",
]
