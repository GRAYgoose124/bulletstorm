import imgui
import imgui.core

from ....gui.widget import Widget


class ShipUiWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(-32, -32, widget_size=widget_size), imgui.ONCE
        )

        with imgui.begin("Ship UI"):
            if imgui.button("Fire Missile"):
                self.button_message = "You fired a missile!"
            if imgui.button("Speak to Ship AI"):
                self.button_message = "Biya! Biya!"
            imgui.text(self.button_message)
            imgui.text(f"Health: {self.page.player.hp}")
