from dataclasses import dataclass, field
import random
from uuid import uuid4

from .stats import ActorStats, Effect, Requirement, Profession
from .gear import GearSet



@dataclass
class Action:
    name: str
    category: str
    description: str
    cost: list[tuple[str, int]] = field(default_factory=list)
    requirements: list[Requirement] = field(default_factory=list)

    can_target_self: bool = False
    can_target_allies: bool = False
    can_target_enemies: bool = False
    max_targets: int = 1

    permanent_effects_on_target: list[Effect] = field(default_factory=list)
    temporary_effects_on_target: list[Effect] = field(default_factory=list)

    def can_afford(self, actor):
        for cost in self.cost:
            if actor.statistics[cost[0]] < cost[1]:
                return False
        return True
    
    def has_requirements(self, actor):
        for requirement in self.requirements:
            if not requirement.check(actor.statistics):
                return False
        return True

            

@dataclass
class Actor:
    name: str
    id: int = field(default_factory=lambda: uuid4().int)

    level: int = 1
    profession: Profession = field(default_factory=Profession)
    gear: GearSet = field(default_factory=GearSet)
    statistics: ActorStats = field(default_factory=ActorStats.zero)
    actions: list[Action] = field(default_factory=list)

    temporary_statistics: ActorStats = field(default_factory=ActorStats.zero)
    active_effects: list[Effect] = field(default_factory=list)

    def __post_init__(self):
        self.party = None

        # set max stats to current stats
        self.statistics.max_health = self.statistics.health
        self.statistics.max_mana = self.statistics.mana
        self.statistics.max_stamina = self.statistics.stamina

    @property
    def total_stats(self):
        return self.statistics + self.profession.bonus_stats + self.temporary_statistics

    @property
    def possible_actions(self):
        return [action for action in self.actions if action.can_afford(self) and action.has_requirements(self)]

    @property
    def alive(self):
        return self.total_stats.health > 0

    def reset_temp_stats(self):
        self.temporary_statistics = ActorStats.zero()

    def apply_effect(self, effect: Effect):
        if effect.chance is not None and random.random() > effect.chance:
            return
        self.active_effects.append((effect, effect.duration))

    def __repr__(self):
        return f"<Actor: {self.name}>"

    def __hash__(self):
        return self.id

class Enemy(Actor):
    pass

class Hero(Actor):
    pass




