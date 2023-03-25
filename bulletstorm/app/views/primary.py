import math
import time
import arcade
import random
from pathlib import Path


from ...game.entity import Player
from ...game.levels.level import Level


class PrimaryView(arcade.View):
    def __init__(self):
        super().__init__()
        self._game_over = False
        self._restart = False

        self.player = None
        self.level = None

        self.setup()

    def setup(self):
        self._game_over = False
        self._restart = False
        self.player = Player()
        self.level = Level(self)

    def end_game(self):
        self._game_over = time.time()
        self.window.show_view("game_over")

    def restart_game(self):
        self.end_game()
        self._restart = True

        self.setup()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        if self._restart:
            self.level.setup(*self.window.get_size())
            self._restart = False

    def on_draw(self):
        arcade.start_render()

        self.level.draw()

    def on_update(self, delta_time: float):
        self.level.update(delta_time)

    def on_resize(self, width: int, height: int):
        self.level.resize(width, height)

    def on_key_press(self, key, modifiers):
        self.__key_handler(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.__key_handler(key, modifiers, release=True)

    def __key_handler(self, key, modifiers, release=False):
        """ Unified key handler for key presses and releases. """
        if key == self.player.keybinds["PLAYER_MOVE_FORWARD"]:
            self.player.acceleration[1] = 0 if release else self.player.keybind_settings['PLAYER_FORWARD_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_MOVE_BACKWARD"]:
            self.player.acceleration[1] = 0 if release else - \
                self.player.keybind_settings['PLAYER_FORWARD_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_MOVE_LEFT"]:
            self.player.acceleration[0] = 0 if release else - \
                self.player.keybind_settings['PLAYER_LATERAL_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_MOVE_RIGHT"]:
            self.player.acceleration[0] = 0 if release else self.player.keybind_settings['PLAYER_LATERAL_ACCELERATION']
        elif key == self.player.keybinds["PLAYER_TURN_LEFT"]:
            self.player.change_angle = 0 if release else self.player.keybind_settings[
                'PLAYER_TURN_VELOCITY']
        elif key == self.player.keybinds["PLAYER_TURN_RIGHT"]:
            self.player.change_angle = 0 if release else - \
                self.player.keybind_settings['PLAYER_TURN_VELOCITY']
        elif key == self.player.keybinds["PLAYER_SHOOT"]:
            # self.player.is_firing = not release
            self.player.shoot()
        elif key == self.player.keybinds["PAUSE_MENU"]:
            if not release:
                self.window.show_view("pause")
