from dataclasses import dataclass, field

from .actor import Actor, ActorStats


class Party:
    """A party is a group of actors."""

    def __init__(self, name: str = None):
        self.name = name
        self.actors = []

    def add_actor(self, actor: Actor):
        actor.party = self
        self.actors.append(actor)

    def remove_actor(self, actor: Actor):
        self.actors.remove(actor)

    def __iter__(self):
        return iter(self.actors)

    def __len__(self):
        return len(self.actors)

    def __getitem__(self, index):
        return self.actors[index]

    def __contains__(self, actor):
        return actor in self.actors

    def __repr__(self):
        return f"<Party: {self.actors}>"

    @property
    def alive(self):
        return any(actor.alive for actor in self.actors)


class HeroParty(Party):
    pass


class EnemyParty(Party):
    pass
