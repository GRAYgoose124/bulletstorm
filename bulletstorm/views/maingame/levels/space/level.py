import random, arcade, math
from pathlib import Path
from numba import jit

from .....core.level.base import LevelBase

from .....core.entity.agent.manager import AgentManager
from .....core.entity.manager import EntityAlreadyRemovedError

from ...entities.player.player import SpacePlayer
from ...entities.asteroid import Asteroid
from ...entities.simpleagent import Catcher

from .settings import SpaceGamePlayerSettings


@jit(nopython=True)
def _create_complex_polygon_sprite(
    num_points: int, radius: float, center_x: float, center_y: float
):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))

    return points


def create_complex_polygon_sprite(
    num_points: int, radius: float, center_x: float, center_y: float
):
    points = _create_complex_polygon_sprite(num_points, radius, center_x, center_y)
    return arcade.create_line_generic(points, arcade.color.WHITE)


def spawn_catchers(level):
    default_p = level.manager.get_worldspace_center()

    placed = []
    for _ in range(10):
        p = (
            default_p[0] + random.uniform(-200, 200),
            default_p[1] + random.uniform(-200, 200),
        )
        Catcher.add_to_manager(level.manager, center=p)
        placed.append(p)

    return placed


def spawn_player(level, position: tuple[int, int] = None, mass=1.0):
    # ship sheet has two sprites side by side
    # TODO move into player class and preserve game player
    root = Path(__file__).parents[5] / "assets/topdown-scifi/asteroid-fighter"
    level.player = SpacePlayer(
        SpaceGamePlayerSettings,
        root / "ship.png",
        image_x=0,
        image_y=0,
        image_width=48,
        image_height=48,
    )

    # Set the player in the center of screen / not worldspace
    if position is None:
        h, w = level.manager.get_worldspace_center()
        level.player.center_x = h
        level.player.center_y = w
    else:
        level.player.center_x = position[0]
        level.player.center_y = position[1]

    # Add the player to the manager
    level.manager.add_entity(
        level.player,
        mass=mass,
        tag="player",
        collide_with_own_type=False,
    )

    # Add the player to the entity graph and add collision handler
    level.manager.entity_graph.add_node(level.player)
    level.manager.add_collision_handler(
        "player", "asteroid", level.player.collision_handler
    )

    return level.player


@jit(nopython=True)
def place_asteroids(
    n,
    n_dist,
    max_tries,
    worldspace_dims,
):
    placed = []
    for _ in range(n):
        rx, ry = 0, 0
        tries = 0
        while tries < max_tries:
            rx = random.randint(0, worldspace_dims[0])
            ry = random.randint(0, worldspace_dims[1])

            valid_placement = True
            min_dist = worldspace_dims[0] // n_dist
            for x, y in placed:
                if ((rx - x) ** 2 + (ry - y) ** 2) ** 0.5 <= min_dist:
                    valid_placement = False
                    break

            if valid_placement:
                break
            else:
                tries += 1

        if valid_placement:
            placed.append((rx, ry))

    return placed


def generate_asteroids(level, n=600, n_dist=10, max_tries_recip=2):
    # Create the asteroids
    asteroid_list = [
        ":resources:images/space_shooter/meteorGrey_big1.png",
        ":resources:images/space_shooter/meteorGrey_big2.png",
        ":resources:images/space_shooter/meteorGrey_big3.png",
        ":resources:images/space_shooter/meteorGrey_big4.png",
        ":resources:images/space_shooter/meteorGrey_med1.png",
        ":resources:images/space_shooter/meteorGrey_med2.png",
        ":resources:images/space_shooter/meteorGrey_small1.png",
        ":resources:images/space_shooter/meteorGrey_small2.png",
        ":resources:images/space_shooter/meteorGrey_tiny1.png",
        ":resources:images/space_shooter/meteorGrey_tiny2.png",
    ]

    # Randomly generate the asteroids
    n_dist = n * n_dist
    max_tries = max_tries_recip // 2
    placed = place_asteroids(
        n,
        n_dist,
        max_tries,
        level.manager.worldspace_dims,
    )

    for rx, ry in placed:
        # Create the asteroid
        asset = random.choice(asteroid_list)
        asteroid = Asteroid(asset, 0.5, center_x=rx, center_y=ry)

        if "tiny" in asset:
            m = 0.3 + random.uniform(-0.2, 0.2)
            velocity = [random.uniform(-8, 8), random.uniform(-8, 8)]
        elif "small" in asset:
            m = 0.7 + random.uniform(-0.2, 0.2)
            velocity = [random.uniform(-4, 4), random.uniform(-4, 4)]
        elif "med" in asset:
            m = 1.5 + random.uniform(-0.2, 0.2)
            velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        elif "big" in asset:
            m = 3.3 + random.uniform(-0.2, 0.2)
            velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

        level.manager.add_entity(
            asteroid,
            tag="asteroid",
            mass=m,
        )

        asteroid.hp = m * 5
        body = level.manager.get_physics_object(asteroid).body
        body.velocity = velocity
        body.angular_velocity = random.uniform(-1, 1)
        body.friction = 0.0


class SpaceLevel(LevelBase):
    def setup(self):
        self.manager = AgentManager(self.parent, worldspace_type="wrapping")

        spawn_player(self)
        spawn_catchers(self)
        generate_asteroids(self)

    def update_level(self, delta_time):
        # self._update_asteroids()
        pass

    def _update_asteroids(self):
        # move all the asteroids
        for asteroid in self.manager.by_tag("asteroid"):
            try:
                body = self.manager.get_physics_object(asteroid).body
            except EntityAlreadyRemovedError:
                continue

            force = [random.uniform(-100, 100), random.uniform(-100, 100)]

            self.manager.apply_force(asteroid, force)
