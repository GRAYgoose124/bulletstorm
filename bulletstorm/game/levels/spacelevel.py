import arcade
import random
from pathlib import Path

from pymunk import Vec2d

from bulletstorm.game.entity import EntityManager, Player
from bulletstorm.game.entity.core.manager import EntityAlreadyRemovedError

from bulletstorm.game.entity.asteroid import Asteroid


class SpaceLevel:
    def __init__(self, parent):
        self.parent = parent

        self._player = parent.player
        self.manager = None

        self.size = None
        self.resize(*parent.window.get_size())
        self.setup()

    def setup(self):
        self.manager = EntityManager(self.parent)

        self.__spawn_player()
        self.__generate_asteroids()

    def resize(self, width, height):
        self.size = (width, height)
        # self.setup()

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value
        self.parent.player = value

    def __spawn_player(self, position: tuple[int, int] = None, mass=1.0):
        # ship sheet has two sprites side by side
        # TODO move into player class and preserve game player
        root = (
            Path(__file__).parent.parent.parent.parent
            / "assets"
            / "topdown-scifi"
            / "asteroid-fighter"
        )
        self.player = Player(
            root / "ship.png", image_x=0, image_y=0, image_width=48, image_height=48
        )

        # Set the player in the center
        if position is None:
            self.player.center_x = self.size[0] // 2
            self.player.center_y = self.size[1] // 2
        else:
            self.player.center_x = position[0]
            self.player.center_y = position[1]

        self.manager.add_entity(
            self.player,
            mass=mass,
            tag="player",
            collision_type="player",
            collision_type_b="enemy",
        )

    def __generate_asteroids(self):
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
        placed = [(self.player.center_x, self.player.center_y)]
        n = 500
        n_dist = n * 10
        max_tries = n // 2
        for _ in range(n):
            # Try to place the asteroid at a random location
            rx, ry = 0, 0
            tries = 0
            while (
                not all(
                    [
                        ((rx - x) ** 2 + (ry - y) ** 2) ** 0.5
                        > (self.manager.worldspace_dims[0] // n_dist)
                        for x, y in placed
                    ]
                )
                and tries < max_tries
            ):
                rx, ry = random.randint(
                    0, self.manager.worldspace_dims[0]
                ), random.randint(0, self.manager.worldspace_dims[1])
                tries += 1

            # Create the asteroid
            asset = random.choice(asteroid_list)
            asteroid = Asteroid(asset, 0.5, center_x=rx, center_y=ry)
            asteroid.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

            if "tiny" in asset:
                m = 0.3
            elif "small" in asset:
                m = 0.7
            elif "med" in asset:
                m = 1.5
            elif "big" in asset:
                m = 3.3
            asteroid.hp = m * 5

            self.manager.add_entity(
                asteroid,
                tag="asteroid",
                collision_type="enemy",
                collision_type_b="player",
                mass=m,
            )
            placed.append((rx, ry))

    def _update_asteroids(self):
        # move all the asteroids
        for asteroid in self.manager.by_tag("asteroid"):
            try:
                body = self.manager.get_physics_object(asteroid).body
            except EntityAlreadyRemovedError:
                continue

            random_force = [random.uniform(-10, 10), random.uniform(-10, 10)]
            force = [
                body.velocity[0] * random.uniform(0.5, 1.5) or random_force[0],
                body.velocity[1] * random.uniform(0.5, 1.5) or random_force[1],
            ]

            if (force[0] ** 2 + force[1] ** 2) > 1000:
                force = [0.0, 0.0]

            self.manager.apply_force(asteroid, force)

    def update(self, delta_time: float):
        self._update_asteroids()

        # run the physics update
        self.manager.step(delta_time)

        # check if player is dead
        if self.player.hp <= 0:
            self.parent.end_game()

    def draw(self):
        self.manager.draw()
