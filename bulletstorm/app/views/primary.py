import arcade
import random


class PrimaryView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self._restart = False

        self.player_sprite = None
        self.player_velocity = [0, 0]
        self.player_delta = [0, 0]

        self.asteroids = None

        self.generate_level(*self.window.get_size())

    def __reset_game(self):
        self.player_velocity = [0, 0]
        self.player_delta = [0, 0]

    def __end_game(self):
        self.window.show_view("game_over")
        self._restart = True
        self.__reset_game()

    def generate_level(self, width, height):

        # Set the player in the center
        self.player_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip1_blue.png", 0.5)
        self.player_sprite.center_x = width // 2
        self.player_sprite.center_y = height // 2

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
        placed = [(self.player_sprite.center_x, self.player_sprite.center_y)]
        n = 50
        for _ in range(n):
            rx, ry = 0, 0
            while not all([((rx - x) ** 2 + (ry - y) ** 2) ** 0.5 > (width // n) for x, y in placed]):
                rx, ry = random.randint(0, width), random.randint(0, height)
            
            asteroid = arcade.Sprite(random.choice(asteroid_list), 0.5)
            asteroid.center_x = rx
            asteroid.center_y = ry
            placed.append((rx, ry))
            self.asteroids.append(asteroid)


    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        if self._restart:
            self.generate_level(*self.window.get_size())
            self._restart = False

    def on_draw(self):
        arcade.start_render()

        self.player_sprite.draw()
        self.asteroids.draw()

    def on_update(self, delta_time: float):
        # move all the asteroids
        for asteroid in self.asteroids:
            asteroid.center_x += random.randint(-10, 10)
            asteroid.center_y += random.randint(-10, 10)

        # decay the player velocity
        self.player_velocity[0] *= 0.9

        # accelerate the player
        self.player_velocity[0] += self.player_delta[0]
        self.player_velocity[1] += self.player_delta[1] 

        # move the player
        self.player_sprite.center_x += self.player_velocity[0]
        self.player_sprite.center_y += self.player_velocity[1]

        # check for collisions
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.asteroids)

        # if there is a collision, end the game
        if len(hit_list) > 0:
            print("STOP GETTING HIT STUPID")
            # self.__end_game()

    def on_resize(self, width: int, height: int):
        self.generate_level(width, height)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view("pause")

        if key == arcade.key.W:
            self.player_delta[1] = 1
        elif key == arcade.key.S:
            self.player_delta[1] = -1
        elif key == arcade.key.A:
            self.player_delta[0] = -1
        elif key == arcade.key.D:
            self.player_delta[0] = 1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player_delta[1] = 0
        elif key == arcade.key.S:
            self.player_delta[1] = 0
        elif key == arcade.key.A:
            self.player_delta[0] = 0
        elif key == arcade.key.D:
            self.player_delta[0] = 0

        
    
