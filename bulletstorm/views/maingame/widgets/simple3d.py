import arcade, imgui, imgui.core, logging

from ....core.gui.widget import Widget

log = logging.getLogger(__name__)


class Simple3d(Widget):
    def __init__(self, page):
        super().__init__(page, draw_mode=imgui.ONCE)

        self._selected_level = None
        self.

        self.size = (256, 128), (32, -32)

    def draw(self):
        with imgui.begin("3D GL"):
            pass