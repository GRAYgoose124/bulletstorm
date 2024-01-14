from multiprocessing import Process
from .graphline import GraphLineMixin
from .core import Agent, AgentEvent, AgentSpec

from ..manager import EntityManager
from ..base import Entity


class AgentManager(EntityManager, GraphLineMixin):
    def __init__(self, parent) -> None:
        EntityManager.__init__(self, parent)
        GraphLineMixin.__init__(self)

        self.agent_ids = []
        self.agents = {}

        self.agent_update_timer = 0

    def step(self, delta_time):
        super().step(delta_time)
        self._update_lines()

        if self.agent_update_timer <= 0:
            self._update_agent_forces()
            self.agent_update_timer = 0.33
        else:
            self.agent_update_timer -= delta_time

    def draw(self):
        self.graph_line_list.draw()
        super().draw()

    def remove_entity(self, entity: Entity, *args, **kwargs):
        try:
            super().remove_entity(entity, *args, **kwargs)
            self.remove_entity_from_graph(entity)
        except KeyError:
            pass

    def _update_agent_forces(self):
        for agent_id, agent in self.agents.items():
            agent.apply_forces()
