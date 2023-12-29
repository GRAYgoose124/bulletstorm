from ..base import Entity


class AgentForce:
    def apply(self, entity_a: Entity = None, entity_b: Entity = None):
        """Can apply force to entity_a, entity_b, or both"""
        pass


class Agent:
    def __init__(
        self,
        entity_edges: dict[tuple[int], tuple[Entity]] = None,
        forces: dict[tuple[int], AgentForce] = None,
    ):
        self.entity_edges = entity_edges or {}
        self.edge_forces = forces or {}

    @classmethod
    def generate_and_add_agent(
        cls,
        manager: "AgentManager",
        base_entity_cls: type,
        base_args: tuple,
        internal_edges: list[tuple[int]],
        forces: dict[tuple[int], AgentForce] = None,
        center=(0, 0),
    ):
        base_args[1]["hp"] = 50

        nodes = []
        for i, edge in enumerate(internal_edges):
            # update center_x and center_y by scaling by edges
            base_args[1]["center_x"] = center[0] + 50 * (edge[0] + 1)
            base_args[1]["center_y"] = center[1] + 50 * (edge[1] + 1)
            entity = base_entity_cls(*base_args[0], **base_args[1])
            nodes.append(entity)

        for node in nodes:
            manager.add_entity(node, tag="agent")
            manager.entity_graph.add_node(node)

        node_edges = {}
        # use the internal edges to connect the nodes
        for edge in internal_edges:
            ne = (nodes[edge[0]], nodes[edge[1]])
            node_edges[edge] = ne
            manager.add_line_between(*ne)

        return cls(node_edges, forces)

    def apply_forces(self):
        for edge, force in self.edge_forces.items():
            force.apply(*self.entity_edges[edge])
