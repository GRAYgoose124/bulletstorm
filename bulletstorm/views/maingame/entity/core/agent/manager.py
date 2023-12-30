from .graphline import GraphLineMixin
from .core import Agent, AgentForce, AgentSpec

from ..manager import EntityManager
from ..base import Entity


class AgentManager(EntityManager, GraphLineMixin):
    def __init__(self, parent) -> None:
        EntityManager.__init__(self, parent)
        GraphLineMixin.__init__(self)

        self.agent_ids = []
        self.agents = {}

        self.force_timer = 0

    def step(self, delta_time):
        super().step(delta_time)
        self._update_lines()

        if self.force_timer <= 0:
            self._update_agent_forces()
            self.force_timer = 0.33
        else:
            self.force_timer -= delta_time

    def remove_entity(self, entity: Entity, *args, **kwargs):
        try:
            super().remove_entity(entity, *args, **kwargs)
            self.remove_entity_from_graph(entity)
        except KeyError:
            pass

    def add_agent(
        self,
        spec: AgentSpec,
        center: tuple[float, float] = None,
        tag: str = "agent",
    ):
        center = center or self.get_worldspace_center()

        # agent = Agent.generate_and_add_agent(
        #     self, base_entity_cls, base_args, internal_edges, forces, center
        # )
        spec.add_to_manager(self, center)

    def _update_agent_forces(self):
        for agent_id, agent in self.agents.items():
            agent.apply_forces()
