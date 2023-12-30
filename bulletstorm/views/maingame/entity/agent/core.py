from dataclasses import dataclass
from ..base import Entity


class AgentForce:
    def apply(self, entity_a: Entity = None, entity_b: Entity = None):
        """Can apply force to entity_a, entity_b, or both"""
        pass


# def __generate_simple_agent(self):
#     base_entity_cls = Asteroid
#     base_args = (
#         (":resources:images/space_shooter/meteorGrey_big1.png", 0.5),
#         {"center_x": 50, "center_y": 50},
#     )
#     forces = {
#         (0, 1): AgentForce(),
#         (1, 2): AgentForce(),
#         (2, 3): AgentForce(),
#         (3, 0): AgentForce(),
#     }
#     self.manager.add_agent(
#         base_entity_cls, base_args, [(0, 1), (1, 2), (2, 3), (3, 0)], forces
#     )
@dataclass
class AgentSpec:
    base_entity_cls: type
    base_args: tuple
    internal_edges: list[tuple[int]]
    forces: dict[tuple[int], AgentForce]

    def add_to_manager(self, manager: "AgentManager", center=(0, 0)):
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

        node_edges = {}
        # use the internal edges to connect the nodes
        for edge in self.internal_edges:
            ne = (nodes[edge[0]], nodes[edge[1]])
            node_edges[edge] = ne
            manager.add_line_between(*ne)

        # add agent to manager
        agent = Agent(node_edges, self.forces)
        agent_id = len(manager.agent_ids)
        manager.agent_ids.append(agent_id)
        manager.agents[agent_id] = agent


class Agent:
    def __init__(
        self,
        entity_edges: dict[tuple[int], tuple[Entity]] = None,
        forces: dict[tuple[int], AgentForce] = None,
    ):
        self.entity_edges = entity_edges or {}
        self.edge_forces = forces or {}

    def apply_forces(self):
        for edge, force in self.edge_forces.items():
            force.apply(*self.entity_edges[edge])
