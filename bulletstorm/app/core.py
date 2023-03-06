import arcade

from .views import *


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 300, 300, arcade.color.WHITE, 54)

    def on_key_press(self, key, modifiers):
        self.window.show_view("primary")


class BulletStorm(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, 
                         "B. S. - Time to get your degree", 
                         gl_version=(4, 3), 
                         resizable=True)
        self.center_window()
        
        self._views = {
            "primary": PrimaryView(),
            "pause": PauseView(),
            "game_over": GameOverView(),
        }

        self._last_view = None

        self.show_view("primary")

    @property
    def views(self):
        return self._views

    def show_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")
        
        # get the key of the current view
        if (self._current_view is not None and 
            type(self._current_view) in [type(x) for x in self._views.values()]):
            key = {v: k for k, v in self._views.items()}[self._current_view]
            self._last_view = key

        super().show_view(self.views[view])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_view("pause")
