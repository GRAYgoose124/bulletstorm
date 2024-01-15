from pymunk import Vec2d

from ....core.entity.base import Entity
from ....core.entity.agent.core import AgentForce, AgentSpec, AgentCollisionHandler
from .asteroid import Asteroid


class ImpulseOnCollision(AgentCollisionHandler):
    def handle(self, entity_a: Entity, entity_b: Entity, arbiter, space, data):
        # repel the two entities
        force = 1.0

        body_a = entity_a.manager.get_physics_object(entity_a).body
        body_b = entity_b.manager.get_physics_object(entity_b).body

        b_to_a = Vec2d(*entity_a.position) - entity_b.position
        b_to_a = b_to_a.normalized()

        body_a.apply_impulse_at_local_point(-b_to_a * force, (0, 0))
        body_b.apply_impulse_at_local_point(-b_to_a * force, (0, 0))
        return True


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


Catcher = AgentSpec(
    base_entity_cls=Asteroid,
    base_args=(
        (":resources:images/space_shooter/meteorGrey_big1.png", 0.5),
        {"center_x": 50, "center_y": 50, "hp": 50},
    ),
    internal_edges=[(0, 1), (1, 2), (2, 3), (3, 0)],
    forces={
        (0, 1): ConstrictionForce(),
        (1, 2): ConstrictionForce(),
        (2, 3): ConstrictionForce(),
        (3, 0): ConstrictionForce(),
    },
    collision_handlers=[ImpulseOnCollision()],
)
