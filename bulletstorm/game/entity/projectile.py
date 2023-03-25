from .entity import Entity

class Projectile(Entity):
    def __init__(self, *args, **kwargs):
        resource = ":resources:images/space_shooter/laserBlue01.png"
        super().__init__(resource, *args, **kwargs)

    def collision_handler(self, sprite_a, sprite_b, arbiter, space, data):        
        self.manager.remove_entity(sprite_a)
        self.manager.remove_entity(sprite_b)
        return False