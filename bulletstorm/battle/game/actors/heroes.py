from ...core import Hero, ActorStats
from ..actions.attacks import slash_attack


mitochondra_hero = lambda: Hero(
    name="Mitochondra",
    actions=[
        slash_attack,
    ],
    statistics=ActorStats(health=15, stamina=12, mana=15, dexterity=5),
)


__all__ = [
    "mitochondra_hero",
]
