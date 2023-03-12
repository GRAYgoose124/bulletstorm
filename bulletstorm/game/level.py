import arcade
import random
from pathlib import Path


class Level:
    def __init__(self, parent):
        self.parent = parent

        self.player = parent.player
        self.physics_engine = None

        self.size = None
        self.resize(*parent.window.get_size())

    def setup(self):
        self.physics_engine = arcade.PymunkPhysicsEngine()

        self.__spawn_player()
        self.__generate_asteroids()

    def resize(self, width, height):
        self.size = (width, height)

        self.setup()

    def __spawn_player(self, position: tuple[int, int] = None, mass=1.0):
        # ship sheet has two sprites side by side
        root = Path(__file__).parent.parent.parent / "assets" / \
            "topdown-scifi" / "asteroid-fighter"
        self.player.sprite = arcade.Sprite(
            root / "ship.png", image_x=0, image_y=0, image_width=48, image_height=48)

        # Set the player in the center
        if position is None:
            self.player.sprite.center_x = self.size[0] // 2
            self.player.sprite.center_y = self.size[1] // 2
        else:
            self.player.sprite.center_x = position[0]
            self.player.sprite.center_y = position[1]

        self.physics_engine.add_sprite(self.player.sprite, mass=mass)

    def __generate_asteroids(self):
        # Create the asteroids
        self.asteroids = arcade.SpriteList()
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
        placed = [(self.player.sprite.center_x, self.player.sprite.center_y)]
        n = 100
        n_dist = n * 10
        max_tries = n // 2
        for _ in range(n):
            # Try to place the asteroid at a random location
            rx, ry = 0, 0
            tries = 0
            while not all([((rx - x) ** 2 + (ry - y) ** 2) ** 0.5 > (self.size[0] // n_dist) for x, y in placed]) and tries < max_tries:
                rx, ry = random.randint(
                    0, self.size[0]), random.randint(0, self.size[1])
                tries += 1

            # Create the asteroid
            asset = random.choice(asteroid_list)
            asteroid = arcade.Sprite(asset, 0.5)
            asteroid.center_x = rx
            asteroid.center_y = ry
            asteroid.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

            if "tiny" in asset:
                m = 0.3
            elif "small" in asset:
                m = 0.7
            elif "med" in asset:
                m = 1.5
            elif "big" in asset:
                m = 3.3

            # Add the asteroid to the physics engine
            self.physics_engine.add_sprite(asteroid, mass=m)
            # TODO: add a collision handler for the asteroids and the player?
            self.asteroids.append(asteroid)
            placed.append((rx, ry))

    def update(self, delta_time: float):
        # rotate the player
        if self.player.sprite.change_angle != 0:
            body = self.physics_engine.get_physics_object(
                self.player.sprite).body
            body.angle += self.player.sprite.change_angle
            # zero rotation in body acceleration
            body.angular_velocity = 0

        # accelerate the player
        self.physics_engine.apply_impulse(
            self.player.sprite, self.player.acceleration)

        # move all the asteroids
        for asteroid in self.asteroids:
            current_vel = self.physics_engine.get_physics_object(
                asteroid).body.velocity
            random_force = [random.uniform(-1, 1), random.uniform(-1, 1)]
            force = [current_vel[0] * random.uniform(
                0.5, 1.5) or random_force[0], current_vel[1] * random.uniform(0.5, 1.5) or random_force[1]]

            if (force[0]**2 + force[1]**2) > 100:
                force = [0.0, 0.0]

            self.physics_engine.apply_force(asteroid, force)

        # run the physics update
        self.physics_engine.step()

        # check for collisions
        # TODO: add a collision handler for the asteroids and the player?
        hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.asteroids)

        # damage player
        if len(hit_list) > 0:
            self.player.take_damage(25)

        # check if player is dead
        if self.player.hp <= 0:
            self.parent.end_game()

    def draw(self):
        self.asteroids.draw()
        self.player.sprite.draw()
