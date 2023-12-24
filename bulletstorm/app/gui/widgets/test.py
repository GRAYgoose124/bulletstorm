import imgui
import imgui.core

from .core import Widget


class ButtonTestWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(-32, -32, widget_size=widget_size), imgui.ONCE
        )

        with imgui.begin("Widget: Button Test"):
            if imgui.button("Button 1"):
                self.button_message = "You pressed 1!"
            if imgui.button("Button 2"):
                self.button_message = "You pressed 2!"
            imgui.text(str(self.page.player.hp))


from ....battlecore.core import *


class BattleCoreWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""
        self.battle_engine = BattleEngine()

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(512, 512, widget_size=widget_size), imgui.ONCE
        )

        with imgui.begin("Battle Core"):
            imgui.text("Hello, world!")
