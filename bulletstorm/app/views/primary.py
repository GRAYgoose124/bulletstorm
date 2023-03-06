import math
import time
import arcade
import random
from pathlib import Path


class Player:
    def __init__(self):
        self.sprite = None

        self.hp = 100
        self.last_hit = None

        self.acceleration = [0, 0]
        self.rotation = 0

    def reset(self):
        self.hp = 100
        self.last_hit = None

        self.acceleration = [0, 0]
        self.rotation = 0


class PrimaryView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self._restart = False

        self.player = Player()
        self.asteroids = None

        self.physics_engine = None

        self.generate_level(*self.window.get_size())

    def __reset_game(self):
        self.player.reset()

    def __end_game(self):
        self.window.show_view("game_over")
        self._restart = True
        self.__reset_game()

    def generate_level(self, width, height):
        self.physics_engine = arcade.PymunkPhysicsEngine()

        # ship sheet has two sprites side by side
        root = Path(__file__).parent.parent.parent.parent / "assets" / "topdown-scifi" / "asteroid-fighter"
        self.player.sprite = arcade.Sprite(root / "ship.png", image_x=0, image_y=0, image_width=48, image_height=48)

        # Set the player in the center
        self.player.sprite.center_x = width // 2
        self.player.sprite.center_y = height // 2

        self.physics_engine.add_sprite(self.player.sprite, mass=1)

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
        for _ in range(n):
            rx, ry = 0, 0
            while not all([((rx - x) ** 2 + (ry - y) ** 2) ** 0.5 > (width // n) for x, y in placed]):
                rx, ry = random.randint(0, width), random.randint(0, height)
            
            asteroid = arcade.Sprite(random.choice(asteroid_list), 0.5)
            asteroid.center_x = rx
            asteroid.center_y = ry
            placed.append((rx, ry))
            self.asteroids.append(asteroid)

        self.physics_engine.add_sprite_list(self.asteroids, mass=1)


    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        if self._restart:
            self.generate_level(*self.window.get_size())
            self._restart = False

    def on_draw(self):
        arcade.start_render()

        self.player.sprite.draw()
        self.asteroids.draw()

    def on_update(self, delta_time: float):
        # rotate the player
        if self.player.sprite.change_angle != 0:
            self.physics_engine.get_physics_object(self.player.sprite).body.angle += self.player.sprite.change_angle
            
        # accelerate the player
        self.physics_engine.apply_impulse(self.player.sprite, self.player.acceleration)

        # move all the asteroids
        for asteroid in self.asteroids:
            self.physics_engine.apply_force(asteroid, [random.randint(-20, 20), random.randint(-10, 10)])

        # run the physics update
        self.physics_engine.step()

        # check for collisions
        hit_list = arcade.check_for_collision_with_list(self.player.sprite, self.asteroids)

        # damage player
        if len(hit_list) > 0:
            if self.player.last_hit is None or time.time() - self.player.last_hit > 1:
                self.player.hp -= 10
                self.player.last_hit = time.time()
        
        # check if player is dead
        if self.player.hp <= 0:
            self.__end_game()

    def on_resize(self, width: int, height: int):
        self.generate_level(width, height)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view("pause")

        if key == arcade.key.W:
            self.player.acceleration[1] = 1
        elif key == arcade.key.S:
            self.player.acceleration[1] = -1
        elif key == arcade.key.A:
            self.player.acceleration[0] = -1
        elif key == arcade.key.D:
            self.player.acceleration[0] = 1
        elif key == arcade.key.Q:
            self.player.sprite.change_angle = 0.02
        elif key == arcade.key.E:
            self.player.sprite.change_angle = -0.02

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player.acceleration[1] = 0
        elif key == arcade.key.S:
            self.player.acceleration[1] = 0
        elif key == arcade.key.A:
            self.player.acceleration[0] = 0
        elif key == arcade.key.D:
            self.player.acceleration[0] = 0
        elif key == arcade.key.Q:
            self.player.sprite.change_angle = 0
        elif key == arcade.key.E:
            self.player.sprite.change_angle = 0
        
    
