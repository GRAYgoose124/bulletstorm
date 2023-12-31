from dataclasses import dataclass

from ..manager import EntityAlreadyRemovedError
from ..base import Entity


class AgentEvent:
    def __init__(self, involved_tags=None, involved_agent_ids=None):
        self.involved_tags = involved_tags or []
        self.involved_agent_ids = involved_agent_ids or []

    def _handle_involved_tags(self, entity_a, entity_b):
        if any(
            [entity_a.tag in self.involved_tags, entity_b.tag in self.involved_tags]
        ):
            return True
        else:
            return False

    def _handle_involved_ids(self, entity_a, entity_b):
        if any(
            [
                entity_a.entity_id in self.involved_agent_ids,
                entity_b.entity_id in self.involved_agent_ids,
            ]
        ):
            return True
        else:
            return False


class AgentForce(AgentEvent):
    def apply(self, entity_a: Entity = None, entity_b: Entity = None):
        """Can apply force to entity_a, entity_b, or both"""
        pass


class AgentCollisionHandler(AgentEvent):
    def __call__(self, entity_a: Entity, entity_b: Entity, arbiter, space, data):
        """Can apply force to entity_a, entity_b, or both"""
        if self._handle_involved_tags(entity_a, entity_b) or self._handle_involved_ids(
            entity_a, entity_b
        ):
            return self.handle(entity_a, entity_b, arbiter, space, data)
        else:
            return True

    def handle(self, entity_a: Entity, entity_b: Entity, arbiter, space, data):
        pass

    @classmethod
    def adapt_to_given_agents(cls, entities: list[Entity]):
        """Generate a collision handler that will handle collisions between the given entities"""
        return cls(
            involved_agent_ids=[entity.entity_id for entity in entities],
        )


@dataclass
class AgentSpec:
    base_entity_cls: type
    base_args: tuple
    internal_edges: list[tuple[int]]
    forces: dict[tuple[int], AgentEvent]
    collision_handlers: list[AgentCollisionHandler]

    def add_to_manager(self, manager: "AgentManager", center=(0, 0)):
        agent_id = len(manager.agent_ids)

        nodes = []
        for i, edge in enumerate(self.internal_edges):
            # update center_x and center_y by scaling by edges
            self.base_args[1]["center_x"] = center[0] + 50 * (edge[0] + 1)
            self.base_args[1]["center_y"] = center[1] + 50 * (edge[1] + 1)
            entity = self.base_entity_cls(*self.base_args[0], **self.base_args[1])
            nodes.append(entity)

        for node in nodes:
            manager.add_entity(node, tag="agent")
            manager.entity_graph.add_node(node)

        # add collision handlers
        for handler in self.collision_handlers:
            h = handler.adapt_to_given_agents(nodes)
            manager.add_collision_handler("agent", "agent", h)
            manager.add_collision_handler("agent", "asteroid", h)

        node_edges = {}
        # use the internal edges to connect the nodes
        for edge in self.internal_edges:
            ne = (nodes[edge[0]], nodes[edge[1]])
            node_edges[edge] = ne
            manager.add_line_between(*ne)

        # add agent to manager
        agent = Agent(node_edges, self.forces)
        agent.agent_id = agent_id
        manager.agent_ids.append(agent_id)
        manager.agents[agent_id] = agent


class Agent:
    def __init__(
        self,
        entity_edges: dict[tuple[int], tuple[Entity]] = None,
        forces: dict[tuple[int], AgentEvent] = None,
    ):
        self.entity_edges = entity_edges or {}
        self.edge_forces = forces or {}
        self.agent_id = None

    def apply_forces(self):
        try:
            for edge, force in self.edge_forces.items():
                force.apply(*self.entity_edges[edge])
        except EntityAlreadyRemovedError:
            pass
