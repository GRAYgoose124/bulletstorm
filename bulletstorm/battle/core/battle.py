import logging

from dataclasses import dataclass, field

from .actor import Actor, ActorStats
from .party import Party
from .settings import GameSettings


log = logging.getLogger(__name__)


class Battle:
    def __init__(self):
        self.turn = 0
        self.turn_meter = {}

        self.parties: dict[str, Party] = {}
        self.actor_stat_bonuses = {}
        self.actor_status_effects = {}

    @property
    def is_over(self):
        """Check if the battle is over by checing on the "Player" party or all other parties."""
        return not self.parties["Player"].alive or all(
            not party.alive for name, party in self.parties.items() if name != "Player"
        )

    def initialize(self):
        """Initialize the battle."""
        self.turn = 0
        self._initialize_turn_meter()
        self._reset_temp_stats()

    def add_party(self, party: Party):
        self.parties[party.name] = party

    def _initialize_turn_meter(self):
        for actor in self._list_actors(by=None):
            self.turn_meter[actor] = (
                GameSettings.BASE_TURN_METER - actor.total_stats.speed
            )

    def _reset_temp_stats(self):
        for actor in self._list_actors(by=None):
            actor.reset_temp_stats()

    def _list_actors(self, by="speed"):
        """List the actors in the battle."""
        all_actors = [actor for side in self.parties.values() for actor in side]
        if by is None:
            return all_actors
        elif by not in ActorStats.__dataclass_fields__.keys():
            raise ValueError(f"Invalid sorting key: {by}")
        else:
            return sorted(all_actors, key=lambda x: x.total_stats[by])

    def _next_actor(self):
        ready_actor = min(self.turn_meter, key=self.turn_meter.get)
        self.turn_meter[ready_actor] = (
            GameSettings.BASE_TURN_METER - ready_actor.total_stats.speed
        )
        return ready_actor

    def _next_turn(self):
        self.turn += 1
        self._tick_down_turn_meter()
        return self._next_actor()

    def _tick_down_turn_meter(self):
        for actor, meter in self.turn_meter.items():
            self.turn_meter[actor] = max(
                0, meter - actor.total_stats.dexterity * GameSettings.DEX_SCALE
            )

    def pretty_print_battle(self):
        print(f"Turn: {self.turn}")
        for party in self.parties.values():
            print(party.name)
            for actor in party:
                print(f"\t{actor.pretty_stats()}")
