import math
import time
import arcade
import imgui
import random
from pathlib import Path

from ...app.gui.page import Page
from ...game.entity import Player
from ...game.levels.level import SpaceLevel

from ..gui.widgets.test import ButtonTestWidget


class PrimaryView(Page):
    def __init__(self, window, name="primary", title="Primary"):
        super().__init__(window, name, title)
        self._game_over = False
        self._restart = False

        self.player = None
        self.level = None

        self.button_message = ""

        self.add_widget(ButtonTestWidget)
        self.setup()

    def setup(self):
        self._game_over = False
        self._restart = False
        self.player = Player()
        self.level = SpaceLevel(self)

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

    def game_draw(self):
        self.level.draw()

    def gui_draw(self):
        """Page method"""
        imgui.begin("Example: buttons")
        if imgui.button("Button 1"):
            self.button_message = "You pressed 1!"
        if imgui.button("Button 2"):
            self.button_message = "You pressed 2!"
        imgui.text(self.button_message)
        imgui.end()

    def on_update(self, delta_time: float):
        self.level.update(delta_time)
        super().on_update(delta_time)

    def on_hide_view(self):
        return super().on_hide_view()

    def on_resize(self, width: int, height: int):
        self.level.resize(width, height)
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
