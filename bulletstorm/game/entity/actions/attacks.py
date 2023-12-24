import random
import arcade
from ..projectile import Projectile

from ..particles.explosion import make_explosion


def shoot(entity, target_tag="enemy"):
    """Shoots a projectile from the entity, hits target_tags."""
    x, y = entity.center_x, entity.center_y
    projectile = Projectile(
        origin=entity,
        center_x=entity.center_x,
        center_y=entity.center_y,
        angle=entity.angle + 90,
    )
    entity.manager.add_entity(
        projectile,
        collision_type="projectile",
        collision_type_b=target_tag,
        tag="projectile",
        self_collision=False,
    )
    proj = entity.manager.get_physics_object(projectile)
    proj.body.friction = 0

    entity.manager.apply_impulse(
        projectile, [entity.gameplay_settings.PROJECTILE_SPEED, 0]
    )


def shockline(player):
    """Shocks targets connected to the entity."""
    for a, b in player.manager.connected_entities:
        target = None
        if a == player:
            target = b
        elif b == player:
            target = a

        if target is None:
            continue

        # if we kill the enemy, heal
        dmg = random.randint(3, 10)

        # check against old hp just in case something else killed it - prob mitigates most cases
        old_hp = target.hp
        target.take_damage(dmg)
        if target.hp <= 0 and old_hp > 0:
            player.hp += 1
            dmg *= 2

        # spawn explosion at target
        d = player.manager.parent.window.width / 2
        onscreen = target.position - player.position < (d, d)
        if onscreen:
            make_explosion(target, count=dmg * 5)
