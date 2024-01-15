# Game Entities
from .player.player import SpacePlayer
from .asteroid import Asteroid
from .simpleagent import Catcher

spacegame_entities = ["SpacePlayer", "Asteroid", "Catcher"]

__all__ = [*spacegame_entities]
