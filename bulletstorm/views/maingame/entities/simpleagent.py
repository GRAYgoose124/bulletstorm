from pymunk import Vec2d
from ..entity.agent.core import AgentForce, AgentSpec
from .asteroid import Asteroid

# TODO: should be a particle, follow explosion's lead.


class ConstrictionForce(AgentForce):
    def apply(self, node_a, node_b):
        """Apply force to the nodes"""
        force = 100.0
        # node a and b are pymunk objects, for this force, lets draw them nearer to each other slightly
        b_to_a = Vec2d(*node_a.position) - node_b.position
        b_to_a = b_to_a.normalized()

        body_a = node_a.manager.get_physics_object(node_a).body
        body_b = node_b.manager.get_physics_object(node_b).body
        body_a.apply_impulse_at_local_point(-b_to_a * force, (0, 0))
        body_b.apply_impulse_at_local_point(b_to_a * force, (0, 0))


class SimpleAgentSpec(AgentSpec):
    base_entity_cls = Asteroid
    base_args = (
        (":resources:images/space_shooter/meteorGrey_big1.png", 0.5),
        {"center_x": 50, "center_y": 50, "hp": 50},
    )
    internal_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    forces = {
        (0, 1): ConstrictionForce(),
        (1, 2): ConstrictionForce(),
        (2, 3): ConstrictionForce(),
        (3, 0): ConstrictionForce(),
    }

    def __init__(self):
        super().__init__(
            self.base_entity_cls,
            self.base_args,
            self.internal_edges,
            self.forces,
        )


Catcher = SimpleAgentSpec()
