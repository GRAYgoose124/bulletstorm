import random
from pathlib import Path

from ..entity.agent.manager import AgentManager
from ..entity.manager import EntityAlreadyRemovedError

from ..entities.player import Player
from ..entities.asteroid import Asteroid
from ..entities.simpleagent import Catcher


class SpaceLevel:
    def __init__(self, parent):
        self.parent = parent

        self._player = parent.player
        self.manager = None

        self.size = None
        self.resize(*parent.window.get_size())
        self.setup()

    def setup(self):
        self.manager = AgentManager(self.parent)

        self.__spawn_player()
        self.__generate_asteroids()
        self.manager._generate_worldspace_bounds()
        self._update_asteroids()

        self.manager.add_agent(Catcher)

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
            Path(__file__).parents[4] / "assets" / "topdown-scifi" / "asteroid-fighter"
        )
        self.player = Player(
            root / "ship.png", image_x=0, image_y=0, image_width=48, image_height=48
        )

        # Set the player in the center of screen / not worldspace
        if position is None:
            h, w = self.manager.get_worldspace_center()
            self.player.center_x = h
            self.player.center_y = w
        else:
            self.player.center_x = position[0]
            self.player.center_y = position[1]

        self.manager.add_entity(
            self.player,
            mass=mass,
            tag="player",
            collide_with_own_type=False,
        )
        self.manager.entity_graph.add_node(self.player)
        self.manager.add_collision_handler(
            "player", "asteroid", self.player.collision_handler
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
        n = 1200
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
                m = 0.3 + random.uniform(-0.2, 0.2)
            elif "small" in asset:
                m = 0.7 + random.uniform(-0.2, 0.2)
            elif "med" in asset:
                m = 1.5 + random.uniform(-0.2, 0.2)
            elif "big" in asset:
                m = 3.3 + random.uniform(-0.2, 0.2)
            asteroid.hp = m * 5

            self.manager.add_entity(
                asteroid,
                tag="asteroid",
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

            force = [random.uniform(-100, 100), random.uniform(-100, 100)]

            self.manager.apply_force(asteroid, force)

    def update(self, delta_time: float):
        # self._update_asteroids()

        # run the physics update
        self.manager.step(delta_time)

        # check if player is dead
        if self.player.hp <= 0:
            self.parent.end_game()

    def draw(self):
        self.manager.draw()
