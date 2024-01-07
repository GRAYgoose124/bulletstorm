import arcade
import logging
import networkx as nx
from pymunk import Vec2d
import pymunk

from .base import Entity


class EntityAlreadyRemovedError(KeyError):
    pass


class ManagerWorldspaceMixin:
    def __init__(self, *args, **kwargs):
        self.worldspace_dims = (5000, 5000)

    def get_worldspace_center(self):
        return self.worldspace_dims[0] // 2, self.worldspace_dims[1] // 2

    def _wrap_worldspace_body(self, pymunk_obj):
        """Wrap the entity around the worldspace"""
        # if entity outsize the worldbox, wrap it's pos toroidally
        body = pymunk_obj.body
        old_position = body.position
        x, y = old_position.x, old_position.y
        wrapped = False

        if (
            old_position.x > self.worldspace_dims[0]
            or old_position.x > self.worldspace_dims[0]
        ):
            wrapped = True
            x = -x
        if (
            old_position.y > self.worldspace_dims[1]
            or old_position.y > self.worldspace_dims[1]
        ):
            wrapped = True
            y = -y
        body.position = Vec2d(x, y)

        return wrapped

    def _generate_worldspace_bounds(self):
        """Place a box around the worldspace to prevent entities from leaving"""
        width, height = self.worldspace_dims

        # Create the walls
        static_body = self.space.static_body
        static_lines = [
            pymunk.Segment(static_body, (0, 0), (width, 0), 0.0),
            pymunk.Segment(static_body, (width, 0), (width, height), 0.0),
            pymunk.Segment(static_body, (width, height), (0, height), 0.0),
            pymunk.Segment(static_body, (0, height), (0, 0), 0.0),
        ]
        for line in static_lines:
            line.friction = 0.5
            # line.collision_type = "worldspace"
            # line.filter = pymunk.ShapeFilter(categories=0b1 << 1)
        self.space.add(*static_lines)


class EntityManager(arcade.PymunkPhysicsEngine, ManagerWorldspaceMixin):
    def __init__(self, parent) -> None:
        super().__init__()
        ManagerWorldspaceMixin.__init__(self)

        self.parent = parent
        self._entity_list = arcade.SpriteList()
        self._entity_tags = {}

        self.emitter_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()

    @property
    def entities(self):
        return self._entity_list

    def by_tag(self, tag):
        return self._entity_tags.get(tag, [])

    def step(self, delta_time):
        for entity in self._entity_list:
            if entity.hp <= 0:
                self.remove_entity(entity)
                continue
            # if self._wrap_worldspace_body(self.get_physics_object(entity)):
            #     pass
            # self.remove_constraints_on_entity(entity)
            entity.update(delta_time)

        self.explosions_list.update()
        super().step(delta_time)

    def draw(self):
        self.graph_line_list.draw()
        self.entities.draw()
        self.explosions_list.draw()

    def add_entity(
        self,
        entity: Entity,
        *args,
        tag="entity",
        collision_handlers: dict[str, callable] = None,
        collide_with_own_type=True,
        **kwargs
    ):
        entity.manager = self
        entity.tag = tag
        kwargs["collision_type"] = tag

        # also register the self collision handler TODO: it's own method
        if collide_with_own_type:
            self.add_collision_handler(entity.tag, entity.tag, entity.collision_handler)

        if collision_handlers is not None:
            for collision_type, collision_handler in collision_handlers.items():
                self.add_collision_handler(
                    entity.tag, collision_type, collision_handler
                )

        self.add_sprite(entity, *args, **kwargs)
        self._entity_list.append(entity)
        self._entity_tags.setdefault(tag, []).append(entity)
        entity.entity_id = len(self._entity_list) - 1

    def remove_entity(self, entity: Entity, *args, **kwargs):
        try:
            self.remove_sprite(entity, *args, **kwargs)
            self._entity_list.remove(entity)
        except KeyError:
            pass

    def get_physics_object(self, sprite: arcade.Sprite) -> arcade.PymunkPhysicsObject:
        try:
            return super().get_physics_object(sprite)
        except KeyError:
            raise EntityAlreadyRemovedError("Entity has already been removed")
