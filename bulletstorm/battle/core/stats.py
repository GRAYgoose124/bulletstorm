from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ActorStats:
    max_health: int = 10
    max_mana: int = 10
    max_stamina: int = 10

    health: int = 10
    mana: int = 10
    stamina: int = 10

    armor: int = 1

    attack: int = 1
    defense: int = 1
    speed: int = 1

    wisdom: int = 1
    intelligence: int = 1
    charisma: int = 1

    strength: int = 1
    constitution: int = 1
    dexterity: int = 1

    focus: float = 1.0
    rage: float = 1.0
    divinity: float = 1.0
    aspect: float = 1.0

    @classmethod
    def zero(cls, **kwargs):
        zeroed = {k: 0 for k in cls.__annotations__}
        zeroed.update(kwargs)
        return cls(**zeroed)

    @property
    def zeroed(self):
        return self.zero()

    def __add__(self, other):
        return ActorStats(
            **{k: getattr(self, k) + getattr(other, k) for k in self.__annotations__}
        )

    def __sub__(self, other):
        return ActorStats(
            **{k: getattr(self, k) - getattr(other, k) for k in self.__annotations__}
        )

    def __mul__(self, other):
        return ActorStats(**{k: getattr(self, k) * other for k in self.__annotations__})

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return ActorStats(**{k: getattr(self, k) / other for k in self.__annotations__})

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __keys__(self):
        return self.__annotations__.keys()

    def __iter__(self):
        for k in self.__annotations__:
            yield k, getattr(self, k)


@dataclass
class Effect:
    name: str
    description: str

    duration: int | None = None
    chance: float | None = None
    type: Literal["permanent", "temporary"] = "permanent"
    trigger: Literal["on_apply", "on_tick", "on_remove"] = "on_apply"
    
    effects_on_target: ActorStats = field(default_factory=ActorStats.zero)

    def apply(self, actor):
        if self.type == "permanent":
            actor.statistics += self.effects_on_target
        elif self.type == "temporary":
            actor.temporary_statistics += self.effects_on_target

    def remove(self, actor):
        if self.type == "permanent":
            actor.statistics -= self.effects_on_target
        elif self.type == "temporary":
            actor.temporary_statistics -= self.effects_on_target


@dataclass
class Profession:
    bonus_stats: ActorStats = field(default_factory=ActorStats.zero)
    effects: list[Effect] = field(default_factory=list)


@dataclass
class Title:
    name: str
    description: str
    
    bonus_stats: ActorStats = field(default_factory=ActorStats.zero)
    effects: list[Effect] = field(default_factory=list)


@dataclass
class Requirement:
    name: str
    description: str

    stat_requirements: list[tuple[str, int]] = field(default_factory=list)
    gear_requirements: list[tuple[str, int]] = field(default_factory=list)
    profession_requirements: list[str] = field(default_factory=list)
    title_requirements: list[str] = field(default_factory=list)

    def check(self, actor):
        for key, value in self.stat_requirements:
            if key not in actor.statistics.__keys__():
                raise ValueError(f"Invalid requirement: {key}")
            if actor.statistics[key] < value:
                return False
        for key, value in self.gear_requirements:
            if key not in actor.gear.get_items():
                return False
            if actor.gear.get_items()[key].level < value:
                return False
        if self.profession_requirements:
            if actor.profession.name not in self.profession_requirements:
                return False
        if self.title_requirements:
            if actor.title.name not in self.title_requirements:
                return False
        return True