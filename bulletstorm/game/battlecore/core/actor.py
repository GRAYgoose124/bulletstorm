from dataclasses import dataclass, field
from uuid import uuid4

from .stats import ActorStats


@dataclass
class Profession:
    bonus_stats: ActorStats = field(default_factory=ActorStats.zero)


@dataclass
class Action:
    name: str
    category: str
    description: str
    cost: list[tuple[str, int]] = field(default_factory=list)
    temporary_effects_on_target: ActorStats = field(default_factory=ActorStats.zero)
    permanent_effects_on_target: ActorStats = field(default_factory=ActorStats.zero)

    can_target_self: bool = False
    can_target_allies: bool = False
    can_target_enemies: bool = False


@dataclass
class Actor:
    name: str
    id: int = field(default_factory=lambda: uuid4().int)
    profession: Profession = field(default_factory=Profession)
    statistics: ActorStats = field(default_factory=ActorStats.zero)
    temporary_statistics: ActorStats = field(default_factory=ActorStats.zero)

    actions: list[Action] = field(default_factory=list)

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
        return [action for action in self.actions if self.can_afford(action)]

    @property
    def alive(self):
        return self.total_stats.health > 0

    def can_afford(self, action):
        for cost in action.cost:
            if self.statistics[cost[0]] < cost[1]:
                return False
        return True

    def reset_temp_stats(self):
        self.temporary_statistics = ActorStats.zero()

    def pretty_stats(self):
        return f"""
        {self.name}
        Health: {self.total_stats.health}/{self.total_stats.max_health}
        Mana: {self.total_stats.mana}/{self.total_stats.max_mana}
        Stamina: {self.total_stats.stamina}/{self.total_stats.max_stamina}
        
        Attack: {self.total_stats.attack} | Defense: {self.total_stats.defense} | Speed: {self.total_stats.speed}
        Strength: {self.total_stats.strength} | Constitution: {self.total_stats.constitution} | Dexterity: {self.total_stats.dexterity}
        Wisdom: {self.total_stats.wisdom} | Intelligence: {self.total_stats.intelligence} | Charisma: {self.total_stats.charisma}
        Focus: {self.total_stats.focus} | Rage: {self.total_stats.rage} | Divinity: {self.total_stats.divinity} | Aspect: {self.total_stats.aspect}
        """

    def __repr__(self):
        return f"<Actor: {self.name}>"

    def __hash__(self):
        return self.id
