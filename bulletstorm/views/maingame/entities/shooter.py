import math

from .asteroid import Asteroid
from .player.attacks import shoot
from ..levels.space.settings import SGPlayerConfig

from ....core.utils import setup_logging

log = setup_logging(__name__)


class Shooter(Asteroid):
    def __init__(self, *args, **kwargs):
        super().__init__(
            ":resources:images/space_shooter/meteorGrey_tiny1.png",
            0.5,
            hp=50,
            center_x=kwargs["center_x"],
            center_y=kwargs["center_y"],
        )
        self.gameplay_settings = SGPlayerConfig()

    def update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time
        else:
            self.shoot_at_player()

    @staticmethod
    def get_angle_between_vectors(a, b):
        """Calculate the angle between two vectors."""
        # Calculate the differences in coordinates
        delta_x = b[0] - a[0]
        delta_y = b[1] - a[1]

        # Calculate the angle using arctangent
        angle = math.atan2(delta_y, delta_x)
        # Convert angle from radians to degrees
        angle_degrees = math.degrees(angle)

        # Ensure angle is in the range [0, 360)
        if angle_degrees < 0:
            angle_degrees += 360

        return angle_degrees

    def aim_at_entity(self, entity):
        """To aim, the entity must orient towards the entity"""
        # get the vector from the entity to the target
        target = [entity.center_x, entity.center_y]
        self_vector = [self.center_x, self.center_y]

        # get the angle between the two vectors
        angle = self.get_angle_between_vectors(self_vector, target)

        # set the angle of the entity
        self.angle = angle

    def shoot_at_player(self):
        p = self.manager.player

        if p is not None:
            self.aim_at_entity(p)
            shoot(self, target_tag="player")
            self.cooldown = 5
