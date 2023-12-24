import arcade
import logging
import networkx as nx

from .base import Entity


class EntityAlreadyRemovedError(KeyError):
    pass


class EntityManager(arcade.PymunkPhysicsEngine):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self._entity_list = arcade.SpriteList()
        self._entity_tags = {}

        self.entity_graph = nx.Graph()
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
        collision_handler=None,
        collide_with_own_type=True,
        **kwargs
    ):
        if collision_handler is None:
            collision_handler = entity.collision_handler

        if collision_type is not None:
            kwargs["collision_type"] = collision_type

            if collision_type_b is None:
                collision_type_b = collision_type
            else:
                # also register the self collision handler TODO: it's own method
                if collide_with_own_type:
                    self.add_collision_handler(
                        collision_type, collision_type, collision_handler
                    )

            # the other entity's collision handler  will be registered by it's own add_entity call
            self.add_collision_handler(
                collision_type, collision_type_b, collision_handler
            )

        self.add_sprite(entity, *args, **kwargs)
        self._entity_list.append(entity)
        self._entity_tags.setdefault(tag, []).append(entity)

        entity.manager = self
        entity.tag = tag

    def remove_entity_from_graph(self, entity: Entity):
        connected = list(self.entity_graph[entity])
        while len(connected):
            self.entity_graph.remove_edge(entity, connected.pop())

    def remove_entity(self, entity: Entity, *args, **kwargs):
        try:
            self.remove_sprite(entity, *args, **kwargs)
            self._entity_list.remove(entity)
            # remove connected entities
            # find set entries that contain entity
            self.remove_entity_from_graph(entity)
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

    def draw(self):
        # TODO: spritelist sorta thing?
        for entity_a, entity_b in self.entity_graph.edges:
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

    # line stuff
    def add_line_between(self, entity_a: Entity, entity_b: Entity):
        self.entity_graph.add_edge(entity_a, entity_b)

    def has_line(self, entity: Entity):
        return entity in self.entity_graph

    def is_adjacent(self, entity_a: Entity, entity_b: Entity):
        return entity_a in self.entity_graph[entity_b]

    def graph_distance_from(self, entity_a: Entity, entity_b: Entity):
        return nx.shortest_path_length(self.entity_graph, entity_a, entity_b)
