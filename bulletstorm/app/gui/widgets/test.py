import imgui
import imgui.core

from .core import Widget


class ButtonTestWidget(Widget):
    def __init__(self, gui):
        super().__init__(gui)

        self.button_message = ""

    def draw(self):
        imgui.set_next_window_position(self.gui.rel(-32, -32), imgui.ONCE)
        imgui.set_next_window_size(*self.gui.percent_of(0.25, 0.25), imgui.ONCE)
        with imgui.begin("Example: buttons"):
            if imgui.button("Button 1"):
                self.button_message = "You pressed 1!"
            if imgui.button("Button 2"):
                self.button_message = "You pressed 2!"
            imgui.text(self.button_message)


from ....battlecore.core import *


class BattleCoreWidget(Widget):
    def __init__(self, gui):
        super().__init__(gui)

        self.button_message = ""
        self.battle_engine = BattleEngine()

    def draw(self):
        imgui.set_next_window_position(self.gui.rel(32, 32), imgui.ONCE)
        imgui.set_next_window_size(*self.gui.percent_of(0.25, 0.25), imgui.ONCE)
        with imgui.begin("Battle Core"):
            imgui.text("Hello, world!")
