from dataclasses import dataclass, field


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

    def __iter__(self):
        for k in self.__annotations__:
            yield k, getattr(self, k)
