import imgui
from arcade_imgui import ArcadeRenderer

from .page import Page


class Widget:
    def __init__(self, gui):
        self.gui = gui

        self.button_message = ""

    def draw(self):
        imgui.begin("Example: buttons")
        if imgui.button("Button 1"):
            self.button_message = "You pressed 1!"
        if imgui.button("Button 2"):
            self.button_message = "You pressed 2!"
        imgui.text(self.button_message)
        imgui.end()


class Gui:
    def __init__(self, window):
        self.window = window
        self.widgets = [Widget(self)]

        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def _draw_widgets(self):
        for widget in self.widgets:
            widget.draw()

    def draw(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
