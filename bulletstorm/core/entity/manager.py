import time
from typing import Literal
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
        assert isinstance(self, arcade.PymunkPhysicsEngine)
        self.worldspace_dims = (5000, 5000)

    def get_worldspace_center(self):
        return self.worldspace_dims[0] // 2, self.worldspace_dims[1] // 2

    def _is_entity_outside_worldspace(self, entity, padding=0) -> (bool, str):
        """Check if the entity is outside the worldspace and returns which direction"""
        x, y = entity.center_x, entity.center_y
        width, height = self.worldspace_dims
        if x < 0 - padding:
            return True, "left"
        if x > width + padding:
            return True, "right"
        if y < 0 - padding:
            return True, "down"
        if y > height + padding:
            return True, "up"
        return False, None

    def _bound_entity(self, entity, delta_time):
        if self.worldspace_type == "wrapping":
            if entity.last_wrapped is None or entity.last_wrapped <= 0:
                entity.last_wrapped = 1.0
                self._wrap_worldspace_body(entity)
            else:
                entity.last_wrapped -= delta_time

    def _init_entity_bounds(self, entity):
        """Set the entity's bounds to the worldspace"""
        if self.worldspace_type == "wrapping":
            entity.last_wrapped = None

    def _wrap_worldspace_body(self, entity):
        """Wrap the entity around the worldspace using modulo"""
        # if entity outsize the worldbox, wrap it's pos toroidally
        pymunk_obj = self.get_physics_object(
            entity
        )  # coupling forces PymunkPhysicsEngine base class
        body = pymunk_obj.body

        body.position = Vec2d(
            body.position.x % self.worldspace_dims[0],
            body.position.y % self.worldspace_dims[1],
        )

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
    def __init__(
        self,
        parent,
        worldspace_type: Literal["bounded", "wrapping", "no_border"] = "wrapping",
    ):
        super().__init__()
        ManagerWorldspaceMixin.__init__(self)
        self.parent = parent

        if worldspace_type == "bounded":
            self._generate_worldspace_bounds()
        self.worldspace_type = worldspace_type

        self._entity_list = arcade.SpriteList()
        self._entity_tags = {}

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

            self._bound_entity(entity, delta_time)

            entity.update(delta_time)
        super().step(delta_time)

    def draw(self):
        self.entities.draw()

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
            self.add_collision_handler(
                entity.tag,
                entity.tag,
                begin_handler=entity.collision_handler,
                post_handler=entity.post_solve,
            )

        if collision_handlers is not None:
            for collision_type, collision_handler in collision_handlers.items():
                self.add_collision_handler(
                    entity.tag, collision_type, begin_handler=collision_handler
                )

        self.add_sprite(entity, *args, **kwargs)
        self._entity_list.append(entity)
        self._entity_tags.setdefault(tag, []).append(entity)
        entity.entity_id = len(self._entity_list) - 1
        self._init_entity_bounds(entity)

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
