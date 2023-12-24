import arcade
import logging

from .base import Entity


class EntityAlreadyRemovedError(Exception):
    pass


class EntityManager(arcade.PymunkPhysicsEngine):
    def __init__(self) -> None:
        super().__init__()
        self._entity_list = arcade.SpriteList()
        self._entity_tags = {}

        self.connected_entities = set()
        self.explosions_list = arcade.SpriteList()

    @property
    def entities(self):
        return self._entity_list

    def by_tag(self, tag):
        return self._entity_tags.get(tag, [])

    def add_entity(
        self,
        entity: Entity,
        *args,
        tag="entity",
        collision_type=None,
        collision_type_b=None,
        **kwargs
    ):
        if collision_type is not None:
            kwargs["collision_type"] = collision_type

            if collision_type_b is None:
                collision_type_b = collision_type
            else:
                # also register the self collision handler TODO: it's own method
                self.add_collision_handler(
                    collision_type, collision_type, entity.collision_handler
                )

            # the other entity's collision handler  will be registered by it's own add_entity call
            self.add_collision_handler(
                collision_type, collision_type_b, entity.collision_handler
            )

        self.add_sprite(entity, *args, **kwargs)
        self._entity_list.append(entity)
        self._entity_tags.setdefault(tag, []).append(entity)

        entity.manager = self
        entity.tag = tag

    def remove_entity(self, entity: Entity, *args, **kwargs):
        try:
            self.remove_sprite(entity, *args, **kwargs)
            self._entity_list.remove(entity)
            # remove connected entities
            # find set entries that contain entity
            to_remove = set()
            for a, b in self.connected_entities:
                if a == entity or b == entity:
                    to_remove.add((a, b))
            for e in to_remove:
                self.connected_entities.remove(e)

        except KeyError:
            pass

    def get_physics_object(self, sprite: arcade.Sprite) -> arcade.PymunkPhysicsObject:
        try:
            return super().get_physics_object(sprite)
        except KeyError:
            raise EntityAlreadyRemovedError("Entity has already been removed")

    def step(self, delta_time):
        for entity in self._entity_list:
            if entity.hp <= 0:
                self.remove_entity(entity)
            entity.update(delta_time)

        self.explosions_list.update()

        super().step(delta_time)

    def add_line_between(self, entity_a: Entity, entity_b: Entity):
        pair = (entity_a, entity_b)
        if pair not in self.connected_entities:
            self.connected_entities.add(pair)

    def has_line(self, entity: Entity):
        for a, b in self.connected_entities:
            if a == entity or b == entity:
                return True
        return False

    def is_connected(self, entity_a: Entity, entity_b: Entity):
        if any(
            [
                (a == entity_a and b == entity_b) or (a == entity_b and b == entity_a)
                for a, b in self.connected_entities
            ]
        ):
            return True

    def draw(self):
        for entity_a, entity_b in self.connected_entities:
            arcade.draw_line(
                entity_a.center_x,
                entity_a.center_y,
                entity_b.center_x,
                entity_b.center_y,
                arcade.color.WHITE,
                2,
            )
        self.entities.draw()
        self.explosions_list.draw()
