import arcade
import imgui

from arcade_imgui import ArcadeRenderer

from .views import *


class BulletStorm(arcade.Window):
    def __init__(self):
        super().__init__(
            1280,
            720,
            "Bulletstorm: B.S. - Time to get your degree",
            gl_version=(4, 3),
            resizable=True,
        )
        self.center_window()

        # imgui
        imgui.create_context()
        self.renderer = ArcadeRenderer(self)
        self.view_metrics = False

        # pages/views
        self.pages = {}
        self.pages["primary"] = SpaceGameView(self)
        self.pages["pause"] = PauseView()
        self.pages["game_over"] = GameOverView(self)

        self._last_view = None
        self.show_view("primary")

    # window
    @property
    def views(self):
        return self.pages

    def show_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        # get the key of the current view
        if self._current_view is not None and type(self._current_view) in [
            type(x) for x in self.views.values()
        ]:
            key = {v: k for k, v in self.views.items()}[self._current_view]
            self._last_view = key

        super().show_view(self.views[view])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_view("pause")

    def on_draw(self):
        super().on_draw()
        imgui.render()

        # check if window was closed
        if self._current_view is None:
            self.close()
            return

        self.renderer.render(imgui.get_draw_data())

    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

    def on_resize(self, width: int, height: int):
        return super().on_resize(width, height)
