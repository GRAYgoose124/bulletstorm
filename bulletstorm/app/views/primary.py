import math
import time
import arcade
import random
from pathlib import Path


from ...game.entity import Player


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

    def __spawn_player(self, width, height):
        # ship sheet has two sprites side by side
        root = Path(__file__).parent.parent.parent.parent / "assets" / "topdown-scifi" / "asteroid-fighter"
        self.player.sprite = arcade.Sprite(root / "ship.png", image_x=0, image_y=0, image_width=48, image_height=48)

        # Set the player in the center
        self.player.sprite.center_x = width // 2
        self.player.sprite.center_y = height // 2

        self.physics_engine.add_sprite(self.player.sprite, mass=1)

    def __generate_asteroids(self, width, height,):
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
            rx, ry = random.randint(0, width), random.randint(0, height)
            
            asset = random.choice(asteroid_list)
            asteroid = arcade.Sprite(asset, 0.5)
            asteroid.center_x = rx
            asteroid.center_y = ry
            asteroid.velocity = (random.random() * 2 - 1) * 100, (random.random() * 2 - 1) * 100
            placed.append((rx, ry))
            self.asteroids.append(asteroid)

        if "tiny" in asset:
            m = 0.3
        elif "small" in asset:
            m = 0.6
        elif "med" in asset:
            m = 1.2
        elif "big" in asset:
            m = 2.4

        self.physics_engine.add_sprite_list(self.asteroids, mass=1)

    def generate_level(self, width, height):
        self.physics_engine = arcade.PymunkPhysicsEngine()

        self.__spawn_player(width, height)
        self.__generate_asteroids(width, height)

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
            current_vel = self.physics_engine.get_physics_object(asteroid).body.velocity
            random_force = [random.uniform(-1, 1), random.uniform(-1, 1)]
            force = [current_vel[0] * random.uniform(0.5, 1.5) or random_force[0], current_vel[1] * random.uniform(0.5, 1.5) or random_force[1]]

            if (force[0]**2 + force[1]**2) > 100:
                force = [0.0, 0.0]

            self.physics_engine.apply_force(asteroid, force)

        # run the physics update
        self.physics_engine.step()

        # check for collisions
        hit_list = arcade.check_for_collision_with_list(self.player.sprite, self.asteroids)

        # damage player
        if len(hit_list) > 0:
            self.player.take_damage(10)
        
        # check if player is dead
        if self.player.hp <= 0:
            self.__end_game()

    def on_resize(self, width: int, height: int):
        self.generate_level(width, height)

    def on_key_press(self, key, modifiers):
        self.__key_handler(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.__key_handler(key, modifiers, release=True)

    def __key_handler(self, key, modifiers, release=False):
        """ Unified key handler for key presses and releases. """    
        if key == self.player.keybinds["PLAYER_MOVE_FORWARD"]:
            self.player.acceleration[1] = 0 if release else self.player.keybind_settings['PLAYER_FORWARD_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_MOVE_BACKWARD"]:
            self.player.acceleration[1] = 0 if release else -self.player.keybind_settings['PLAYER_FORWARD_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_MOVE_LEFT"]:
            self.player.acceleration[0] = 0 if release else -self.player.keybind_settings['PLAYER_LATERAL_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_MOVE_RIGHT"]:
            self.player.acceleration[0] = 0 if release else self.player.keybind_settings['PLAYER_LATERAL_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_TURN_LEFT"]:
            self.player.sprite.change_angle = 0 if release else self.player.keybind_settings['PLAYER_TURN_VELOCITY']
        elif key == self.player.keybinds["PLAYER_TURN_RIGHT"]:
            self.player.sprite.change_angle = 0 if release else -self.player.keybind_settings['PLAYER_TURN_VELOCITY']
        elif key == self.player.keybinds["PLAYER_SHOOT"]:
            self.player.is_firing = not release
        elif key == self.player.keybinds["PAUSE_MENU"]:
            if not release:
                self.window.show_view("pause")