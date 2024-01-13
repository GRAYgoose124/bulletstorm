import imgui
import imgui.core

from ...gui.widget import Widget


class ShipUiWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""

        self.size = (256, 128), (-308, -32)

    def draw(self):
        with imgui.begin("Ship UI"):
            if imgui.button("Fire Missile"):
                self.button_message = "You fired a missile!"
            if imgui.button("Speak to Ship AI"):
                self.button_message = "Biya! Biya!"
            imgui.text(self.button_message)
            imgui.text(f"Health: {self.page.player.hp}")
