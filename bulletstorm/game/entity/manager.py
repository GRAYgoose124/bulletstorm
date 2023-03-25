import arcade

from .entity import Entity

class EntityManager(arcade.PymunkPhysicsEngine):
    def __init__(self) -> None:
        super().__init__()
        self._sprite_list = arcade.SpriteList()
        self._sprite_tags = {}
         
    @property
    def entities(self):
        return self._sprite_list
    
    def by_tag(self, tag):
        return self._sprite_tags.get(tag, [])
    
    def add_entity(self, entity: Entity, *args, tag="entity", collision_type_b=None, **kwargs):
        if collision_type_b is not None:
            a, b = kwargs["collision_type"], collision_type_b
            if a is None:
                raise ValueError("collision_type must be set if collision_type_b is set")
            self.add_collision_handler(a, b, entity.collision_handler)

        self.add_sprite(entity, *args, **kwargs)
        self._sprite_list.append(entity)
        self._sprite_tags.setdefault(tag, []).append(entity)

        entity.manager = self
        entity.tag = tag

    def remove_entity(self, entity: Entity, *args, **kwargs):
        self.remove_sprite(entity, *args, **kwargs)
        self._sprite_list.remove(entity)
        # remove from tag dict

    def step(self, delta_time):
        for entity in self._sprite_list:
            entity.update(delta_time)

        super().step(delta_time)



    def draw(self):
        self.entities.draw()

