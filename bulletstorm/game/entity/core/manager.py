import arcade

from .base import Entity


class EntityAlreadyRemovedError(Exception):
    pass


class EntityManager(arcade.PymunkPhysicsEngine):
    def __init__(self) -> None:
        super().__init__()
        self._entity_list = arcade.SpriteList()
        self._entity_tags = {}

        self.connected_entities = []

    @property
    def entities(self):
        return self._entity_list

    def by_tag(self, tag):
        return self._entity_tags.get(tag, [])

    def add_entity(
        self, entity: Entity, *args, tag="entity", collision_type_b=None, **kwargs
    ):
        if collision_type_b is not None:
            a, b = kwargs["collision_type"], collision_type_b
            if a is None:
                raise ValueError(
                    "collision_type must be set if collision_type_b is set"
                )
            self.add_collision_handler(a, b, entity.collision_handler)

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
            index = 0
            while index < len(self.connected_entities):
                a, b = self.connected_entities[index]
                if a == entity or b == entity:
                    del self.connected_entities[index]
                else:
                    index += 1

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

        super().step(delta_time)

    def add_line_between(self, entity_a: Entity, entity_b: Entity):
        self.connected_entities.append((entity_a, entity_b))

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
