import random
import arcade
import networkx as nx
import numpy as np

from ...effects.gpu_explosion import make_explosion
from ...entities.projectile import Projectile


def shoot(entity, target_tag="enemy"):
    """Shoots a projectile from the entity, hits target_tags."""
    x, y = entity.center_x, entity.center_y
    angle = entity.angle + 90
    # span in front of the entity using it's angle simply
    x, y = (
        x + np.cos(np.radians(angle)) * 50,
        y + np.sin(np.radians(angle)) * 50,
    )
    projectile = Projectile(
        origin=entity,
        center_x=x,
        center_y=y,
        angle=angle,
    )
    entity.manager.add_entity(
        projectile,
        tag="projectile",
        collide_with_own_type=False,
    )
    entity.manager.add_collision_handler(
        "projectile", "asteroid", projectile.collision_handler
    )
    entity.manager.add_collision_handler(
        "projectile", "agent", projectile.collision_handler
    )

    proj = entity.manager.get_physics_object(projectile)
    proj.body.friction = 0
    # disable all collisions with the entity that spawned it
    #   do it the right way:
    # proj.shapes[0].filter = arcade.ShapeFilter(
    #     categories=arcade.ShapeFilter.ALL_MASKS ^ 0b1 << entity.collision_type
    # )

    entity.manager.apply_impulse(
        projectile, [entity.gameplay_settings.PROJECTILE_SPEED, 0]
    )


# shockline:
def _shockline(player, target, dist):
    dmg = random.randint(1, 7) * dist

    old_hp = target.hp
    target.take_damage(dmg)
    # check against old hp just in case something else killed it - prob mitigates most cases
    if target.hp <= 0 and old_hp > 0:
        # if we kill the enemy, heal
        player.hp += dmg * 0.5
    return dmg


def shockline(player):
    """shocks targets connected to the entity by graph distance from player - farther == more damage"""
    if player not in player.manager.entity_graph:
        return

    me = lambda t: make_explosion(
        t,
        count=dmg * 50,
        screen_origin=(
            -player.manager.parent.camera_sprites.position[0],  # x
            -player.manager.parent.camera_sprites.position[1],  # y
        ),
    )

    for a, b in nx.dfs_edges(
        player.manager.entity_graph,
        source=player,
        depth_limit=player.gameplay_settings.SHOCKLINE_DEPTH,
    ):
        if a != player:
            dmg = _shockline(player, a, player.manager.graph_distance_from(player, a))
            me(a)
        if b != player:
            dmg = _shockline(player, b, player.manager.graph_distance_from(player, b))
            me(b)


def tighten(player):
    """tightens the graph around the player"""
    if player not in player.manager.entity_graph:
        return

    # apply constricting force to all nodes
    for node in player.manager.entity_graph.nodes:
        if node == player:
            continue

        # get the vector from the player to the node
        vec = np.array(node.position) - np.array(player.position)
        # normalize it
        vec = vec / np.linalg.norm(vec)
        # apply force
        player.manager.apply_force(node, (vec * 1000).tolist())
