import arcade
import logging
import networkx as nx
from pymunk import Vec2d

from .base import Entity


class EntityAlreadyRemovedError(KeyError):
    pass


class GraphLineMixin:
    def __init__(self, *args, **kwargs):
        self.graph_line_list = arcade.ShapeElementList()
        self.entity_graph = nx.Graph()
        self.edge_to_line = {}
        self.cached_edge_colors = {}
        self.max_lines = 500

        # Shockline could probably provide all... hrm refactor pl0x

    def _update_lines(self):
        # Update or create lines for each edge
        self.graph_line_list = arcade.ShapeElementList()
        for edge in self.entity_graph.edges:
            entity_a, entity_b = edge
            if (entity_b, entity_a) in self.edge_to_line:
                continue
            # if len(self.graph_line_list) > self.max_lines:
            #     break

            # If the edge is new, create a line and add it to the dictionary
            x1, y1, x2, y2 = (
                entity_a.center_x,
                entity_a.center_y,
                entity_b.center_x,
                entity_b.center_y,
            )

            # distance_between = (x1 - x2) ** 2 + (y1 - y2) ** 2
            # if distance_between > self.parent.window.width**2:
            #     continue

            # create color based on entity graph dist from self.player, a or be could both be non players
            # bad coupling this line stuff needs to be moved
            if edge in self.cached_edge_colors:
                color = self.cached_edge_colors[edge]
            else:
                color = self.cache_new_color(edge, entity_a, entity_b)

            line = arcade.create_line(x1, y1, x2, y2, color, 2)
            self.graph_line_list.append(line)
            self.edge_to_line[edge] = line
        self.uncache_invalidated_colors()

    def cache_new_color(self, edge, entity_a, entity_b):
        a_gd, b_gd = 0, 0
        if entity_a.tag != "player":
            if nx.has_path(self.entity_graph, entity_a, self.parent.player):
                a_gd = self.graph_distance_from(entity_a, self.parent.player)
        if entity_b.tag != "player":
            if nx.has_path(self.entity_graph, entity_b, self.parent.player):
                b_gd = self.graph_distance_from(entity_b, self.parent.player)

        color = (
            (64 * a_gd) % 255,
            (96 * b_gd) % 255,
            255 - 72 * (a_gd + b_gd) % 255,
        )
        self.cached_edge_colors[edge] = color

        return color

    def uncache_invalidated_colors(self):
        # uncache colors for edges that no longer exist
        for edge in list(self.cached_edge_colors.keys()):
            if edge not in self.entity_graph.edges:
                del self.cached_edge_colors[edge]

    # def invalidate_colors(self, entities):
    #     # invalidate colors for edges that contain entity
    #     for edge in self.entity_graph.edges:
    #         if any(
    #             entity in edge and edge in self.cached_edge_colors
    #             for entity in entities
    #         ):
    #             del self.cached_edge_colors[edge]

    def invalidate_all_disjoint_colors(self):
        for edge in self.entity_graph.edges:
            if edge in self.cached_edge_colors:
                if not nx.has_path(self.entity_graph, self.parent.player, edge[0]):
                    del self.cached_edge_colors[edge]
                elif not nx.has_path(self.entity_graph, self.parent.player, edge[1]):
                    del self.cached_edge_colors[edge]

    def remove_entity_from_graph(self, entity: Entity):
        connected = list(self.entity_graph[entity])
        while len(connected):
            self.entity_graph.remove_edge(entity, connected.pop())

        self.entity_graph.remove_node(entity)

    def add_line_between(self, entity_a: Entity, entity_b: Entity):
        self.invalidate_all_disjoint_colors()
        self.entity_graph.add_edge(entity_a, entity_b)

    def has_line(self, entity: Entity):
        return entity in self.entity_graph

    def is_adjacent(self, entity_a: Entity, entity_b: Entity):
        return entity_a in self.entity_graph[entity_b]

    def graph_distance_from(self, entity_a: Entity, entity_b: Entity):
        return nx.shortest_path_length(self.entity_graph, entity_a, entity_b)


class EntityManager(arcade.PymunkPhysicsEngine, GraphLineMixin):
    def __init__(self, parent) -> None:
        super().__init__()
        GraphLineMixin.__init__(self)

        self.parent = parent
        self._entity_list = arcade.SpriteList()
        self._entity_tags = {}

        self.worldspace_dims = (5000, 5000)

        self.emitter_list = arcade.SpriteList()
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

    def _wrap_worldspace_body(self, pymunk_obj):
        """Wrap the entity around the worldspace"""
        # if entity outsize the worldbox, wrap it's pos toroidally
        body = pymunk_obj.body
        old_position = body.position
        x, y = old_position.x, old_position.y

        if (
            old_position.x > self.worldspace_dims[0]
            or old_position.x > self.worldspace_dims[0]
        ):
            x = -x
        if (
            old_position.y > self.worldspace_dims[1]
            or old_position.y > self.worldspace_dims[1]
        ):
            y = -y
        body.position = Vec2d(x, y)

    def step(self, delta_time):
        for entity in self._entity_list:
            if entity.hp <= 0:
                self.remove_entity(entity)
                continue
            self._wrap_worldspace_body(self.get_physics_object(entity))
            entity.update(delta_time)

        self._update_lines()
        self.explosions_list.update()
        super().step(delta_time)

    def draw(self):
        self.graph_line_list.draw()
        self.entities.draw()
        self.explosions_list.draw()
