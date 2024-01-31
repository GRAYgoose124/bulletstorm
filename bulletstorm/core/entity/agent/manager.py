import networkx as nx

from multiprocessing import Process
from .graphline import GraphLineMixin
from .core import Agent, AgentEvent, AgentSpec

from ..manager import EntityManager
from ..base import Entity


class AgentManager(EntityManager, GraphLineMixin):
    def __init__(self, parent, worldspace_type="none"):
        EntityManager.__init__(self, parent, worldspace_type)
        GraphLineMixin.__init__(self, worldspace_dims=self.worldspace_dims)

        self.agent_ids = []
        self.agents = {}

        self.agent_update_timer = 0

    def step(self, delta_time):
        self._update_lines(
            wrapping=True if self.worldspace_type == "wrapping" else False
        )

        if self.agent_update_timer <= 0:
            self._update_agent_forces()
            self.agent_update_timer = 0.33
        else:
            self.agent_update_timer -= delta_time

        super().step(delta_time)

    def draw(self):
        self.graph_line_list.draw()
        super().draw()

    def remove_entity(self, entity: Entity, *args, **kwargs):
        try:
            super().remove_entity(entity, *args, **kwargs)
            self.remove_entity_from_graph(entity)
        except KeyError:
            pass

    def _wrap_worldspace_body(self, entity):
        if entity not in self.entity_graph:
            return super()._wrap_worldspace_body(entity)
        else:
            self._wrap_worldspace_subgraph_entity(entity)

    def _wrap_worldspace_subgraph_entity(self, entity):
        """Because we are wrapping, we need to wait for all entities in the subgraph to exit the worldspace"""
        # get nx subgraph containing entity
        subgraph = nx.descendants(self.entity_graph, entity)
        subgraph.add(entity)

        # check if all entities are outside the worldspace
        for entity in subgraph:
            outside, direction = self._is_entity_outside_worldspace(entity)
            if not outside:
                return

        # wrap the subgraph only if all entities are outside the worldspace
        for entity in subgraph:
            super()._wrap_worldspace_body(entity)

    def _update_agent_forces(self):
        for agent_id, agent in self.agents.items():
            agent.apply_forces()
