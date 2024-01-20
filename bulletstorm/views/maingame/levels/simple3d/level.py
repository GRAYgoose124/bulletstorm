import random
from pathlib import Path
from numba import jit

from .....core.level.base import LevelBase

from .....core.entity.agent.manager import AgentManager
from .....core.entity.manager import EntityAlreadyRemovedError


class Simple3dLevel(LevelBase):
    def setup(self):
        pass

    def update_level(self, delta_time):
        pass
