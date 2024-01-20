from pathlib import Path
import time, arcade, imgui, logging

from ...core.gui.view import GuiView
from ...core.shader.view_mixin import ShaderViewMixin
from ...core.level.view_mixin import LevelViewMixin

from .effects.gpu_explosion import GpuBurst
from .effects.vector_field import VectorFieldShader

from .widgets.spacebattle import ShipUiWidget
from .widgets.battlecore import BattleCoreWidget
from .widgets.debug_lvl_select import DebugLevelSelect

from .levels.space.level import SpaceLevel

log = logging.getLogger(__name__)


class SpaceGameView(GuiView, ShaderViewMixin, LevelViewMixin):
    def __init__(self, window, name="primary", title="Primary"):
        super().__init__(window, name, title)
        ShaderViewMixin.__init__(self)
        LevelViewMixin.__init__(self)

        self.add_shader(GpuBurst)
        # self.add_shader(VectorFieldShader)

        self.add_widget(ShipUiWidget)
        self.add_widget(BattleCoreWidget)
        self.add_widget(DebugLevelSelect)

        self.select_level(SpaceLevel)
        # self.shaders["VectorFieldShader"].set_entity_list(self.level.manager.entities)
        self.load_shadertoy(
            Path(__file__).parent / "effects/shaders/raycasted_shadow_frag.glsl"
        )

    def end_game(self):
        LevelViewMixin.end_game(self)
        self.window.show_view("game_over")

        if self._restart:
            self.init_level()
            self.window.show_view("primary")

    def draw_sidebar(self):
        pos = 16, 32
        imgui.set_next_window_position(*pos, imgui.ONCE)
        widget_size = self.percent_of(0.15, 0.33)
        widget_size = widget_size[0] - 2 * pos[0], widget_size[1] - 2 * pos[1]
        imgui.set_next_window_size(*widget_size, imgui.ONCE)

        with imgui.begin("Controls"):
            imgui.text(self.player_controls_str)

    def draw_game(self):
        self.level.draw()
        self.draw_shadertoy()
        self.player.draw()

        for shader in self.shaders.values():
            shader.draw()

    def draw_gui(self):
        """Page method"""
        pass

    def update(self, delta_time: float):
        player_center = (
            self.player.center_x - self.window.width / 2,
            self.player.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(player_center, 1.0)
        self.camera_sprites.update()

        ShaderViewMixin.update(self, delta_time)
        LevelViewMixin.update(self, delta_time)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        if self._restart:
            self.level.setup(*self.window.get_size())
            self._restart = False

    def on_quit(self):
        self.window.close()

    def on_resize(self, width: int, height: int):
        LevelViewMixin.on_resize(self, width, height)
        ShaderViewMixin.on_resize(self, width, height)
        GuiView.on_resize(self, width, height)

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
