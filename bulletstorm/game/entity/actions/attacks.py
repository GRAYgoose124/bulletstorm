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


def shockline(entity):
    """Shocks targets connected to the entity."""
    for a, b in entity.manager.connected_entities:
        target = None
        if a == entity:
            target = b
        elif b == entity:
            target = a

        if target is None:
            continue

        # if we kill the enemy, heal
        target.take_damage(3)
        if target.hp <= 0:
            entity.hp += 1
            make_explosion(target)

        # spawn explosion at target
        make_explosion(target)
