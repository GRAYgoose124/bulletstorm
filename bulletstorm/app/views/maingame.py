import math
import time
import arcade
import imgui
import random
from pathlib import Path

from ..gui.page import Page
from ...game.entity import Player
from ...game.levels.level import SpaceLevel

from ..gui.widgets.spacebattle import ShipUiWidget
from ..gui.widgets.battlecore import BattleCoreWidget


class SpaceGameView(Page):
    def __init__(self, window, name="primary", title="Primary"):
        super().__init__(window, name, title)
        self._game_over = False
        self._restart = False

        self.player = None
        self.level = None

        self.add_widget(ShipUiWidget)
        self.add_widget(BattleCoreWidget)
        self.setup()

    def setup(self):
        self._game_over = False
        self._restart = False
        self.level = SpaceLevel(self)
        self.player = self.level.player

    def end_game(self):
        self._game_over = time.time()
        self.window.show_view("game_over")

    def restart_game(self):
        self.end_game()
        self._restart = True
        self.setup()

        self.window.show_view("primary")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        if self._restart:
            self.level.setup(*self.window.get_size())
            self._restart = False

    def draw_sidebar(self):
        pos = 16, 32
        imgui.set_next_window_position(*pos, imgui.ONCE)
        widget_size = self.percent_of(0.25, 1.0)
        widget_size = widget_size[0] - 2 * pos[0], widget_size[1] - 2 * pos[1]
        imgui.set_next_window_size(*widget_size, imgui.ONCE)

        with imgui.begin("Controls"):
            imgui.text("V - shockline\nSPACE - fire\n\nESC - pause\n")

    def game_draw(self):
        player_center = (
            self.player.center_x - self.window.width / 2,
            self.player.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(player_center, 0.9)
        self.level.draw()

    def gui_draw(self):
        """Page method"""
        pass

    def on_quit(self):
        self.window.close()

    def on_update(self, delta_time: float):
        self.level.update(delta_time)
        super().on_update(delta_time)

    def on_hide_view(self):
        return super().on_hide_view()

    def on_resize(self, width: int, height: int):
        self.level.resize(width, height)
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
        super().on_resize(width, height)

    def on_key_press(self, key, modifiers):
        self.__key_handler(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.__key_handler(key, modifiers, release=True)

    def __key_handler(self, key, modifiers, release=False):
        """Unified key handler for key presses and releases."""
        self.player.key_handler(key, modifiers, release=release)

        if key == self.player.keybinds.PAUSE_MENU:
            if not release:
                self.window.show_view("pause")
