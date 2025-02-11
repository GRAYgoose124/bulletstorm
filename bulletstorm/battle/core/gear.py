from dataclasses import dataclass, field

from .stats import ActorStats, Effect, Requirement


@dataclass
class Gear:
    name: str
    description: str
    level: int
    requirements: list[Requirement] = field(default_factory=list)

    bonus_stats: ActorStats = field(default_factory=ActorStats.zero)
    effects: list[Effect] = field(default_factory=list)

    def can_equip(self, actor):
        for requirement in self.requirements:
            if not requirement.check(actor):
                return False
        return True


class Helmet(Gear):
    pass

class Armor(Gear):
    pass 

class Gloves(Gear):
    pass

class Boots(Gear):
    pass

class Weapon(Gear):
    pass

class Shield(Gear):
    pass


@dataclass
class GearSet:
    name: str = "Empty Gear Set"
    description: str = "An empty gear set."

    helmet: Helmet | None = None
    armor: Armor | None = None
    gloves: Gloves | None = None
    boots: Boots | None = None
    weapon: Weapon | None = None
    shield: Shield | None = None

    def get_bonus_stats(self):
        return sum([item.bonus_stats for item in self.get_items() if item is not None])
    
    def get_effects(self):
        return sum([item.effects for item in self.get_items() if item is not None])
    
    def get_requirements(self):
        return sum([item.requirements for item in self.get_items() if item is not None])
    
    def get_items(self):
        return [self.helmet, self.armor, self.gloves, self.boots, self.weapon, self.shield]
    