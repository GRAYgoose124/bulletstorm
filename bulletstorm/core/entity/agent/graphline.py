import arcade
import networkx as nx
import pymunk
from ..base import Entity

DYNAMIC_GRAPH_COLORS = False


class GraphLineMixin:
    def __init__(self, *args, **kwargs):
        self.graph_line_list = arcade.ShapeElementList()
        self.entity_graph = nx.Graph()
        self.edge_to_line = {}
        self.cached_edge_colors = {}
        self.constraints = {}
        self.max_lines = 1500

        if "worldspace_dims" in kwargs:
            self.worldspace_dims = kwargs["worldspace_dims"]
        else:
            self.worldspace_dims = None

        # Shockline could probably provide all... hrm refactor pl0x

    def _update_lines(self, wrapping=False):
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
            if DYNAMIC_GRAPH_COLORS:
                if edge in self.cached_edge_colors:
                    color = self.cached_edge_colors[edge]
                else:
                    color = self.cache_new_color(edge, entity_a, entity_b)
            else:
                color = arcade.color.BABY_POWDER

            line = arcade.create_line(x1, y1, x2, y2, color, 2)
            self.graph_line_list.append(line)
            self.edge_to_line[edge] = line

        if DYNAMIC_GRAPH_COLORS:
            self.uncache_invalidated_colors()

    def cache_new_color(self, edge, entity_a, entity_b):
        a_gd, b_gd = 0, 0
        if entity_a.tag != "player":
            if self.parent.player in self.entity_graph and nx.has_path(
                self.entity_graph, entity_a, self.parent.player
            ):
                a_gd = self.graph_distance_from(entity_a, self.parent.player)
        if entity_b.tag != "player":
            if self.parent.player in self.entity_graph and nx.has_path(
                self.entity_graph, entity_b, self.parent.player
            ):
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
                if (
                    self.parent.player not in self.entity_graph
                    or not nx.has_path(self.entity_graph, self.parent.player, edge[0])
                    or not nx.has_path(self.entity_graph, self.parent.player, edge[1])
                ):
                    del self.cached_edge_colors[edge]

    def remove_constraints_on_entity(self, entity):
        for edge in list(self.constraints):
            if entity in edge:
                self.space.remove(self.constraints[edge])
                del self.constraints[edge]

    def remove_edges_to_entity_from_graph(self, entity):
        connected = list(self.entity_graph[entity])
        while len(connected):
            edge = (entity, connected.pop())
            self.entity_graph.remove_edge(*edge)

    def remove_entity_from_graph(self, entity: Entity):
        self.remove_edges_to_entity_from_graph(entity)
        self.remove_constraints_on_entity(entity)
        self.entity_graph.remove_node(entity)

    def add_line_between(self, entity_a: Entity, entity_b: Entity):
        self.invalidate_all_disjoint_colors()

        # if entity_a != self.parent.player and entity_b != self.parent.player:
        # bad coupling
        ba = self.get_physics_object(entity_a).body
        bb = self.get_physics_object(entity_b).body
        # TODO: custom rather than default
        c = pymunk.DampedSpring(
            ba,
            bb,
            (0, 0),
            (0, 0),
            ba.mass * bb.mass * 10,
            1.0,
            1.0,
        )
        self.space.add(c)
        self.constraints[(entity_a, entity_b)] = c
        self.entity_graph.add_edge(entity_a, entity_b)

    def remove_line_from(self, entity_a: Entity, entity_b: Entity):
        success = 0
        edge = (entity_a, entity_b)
        if edge in self.constraints:
            self.space.remove(self.constraints[edge])
            del self.constraints[edge]
            self.entity_graph.remove_edge(*edge)
            success += 1

        if edge in self.edge_to_line:
            del self.edge_to_line[edge]
            success += 1

        if DYNAMIC_GRAPH_COLORS:
            if edge in self.cached_edge_colors:
                del self.cached_edge_colors[edge]
                # success += 1

        return success == 2

    def has_line(self, entity: Entity):
        return entity in self.entity_graph

    def is_adjacent(self, entity_a: Entity, entity_b: Entity):
        return entity_a in self.entity_graph[entity_b]

    def graph_distance_from(self, entity_a: Entity, entity_b: Entity):
        return nx.shortest_path_length(self.entity_graph, entity_a, entity_b)
