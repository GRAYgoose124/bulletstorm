import imgui, imgui.core, logging

from .base import Widget
from ..levels import all_levels

log = logging.getLogger(__name__)


class DebugLevelSelect(Widget):
    def __init__(self, page):
        super().__init__(page, draw_mode=imgui.ONCE)

        self._selected_level = None

        self.size = (256, 128), (32, -32)

    def draw(self):
        with imgui.begin("Levels"):
            for level in all_levels:
                if imgui.button(level.__name__):
                    self.page.restart_game()
                    self.page.select_level(level)
                    self._selected_level = level
                    log.info(f"Selected level {level.__name__}")
                    # self.page.restart_game()
                if self._selected_level == level:
                    imgui.same_line()
                    imgui.text("Selected")
