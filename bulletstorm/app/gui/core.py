import imgui
from arcade_imgui import ArcadeRenderer


class Gui:
    def __init__(self, window):
        self.window = window

        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def draw(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def rel(self, x, y):
        """Converts relative coordinates to window coordinates

        Args:
            x (int): x coordinate offset, negatives are allowed and go from right to left
            y (_type_): y coordinate offset, negatives are allowed and go from bottom to top
        """
        if x < 0:
            x = self.window.width + x
        if y < 0:
            y = self.window.height + y
        return x, y

    def percent_of(self, x, y):
        """Converts percentage of window to window coordinates

        Args:
            x (int): percentage of window width
            y (int): percentage of window height
        """
        return self.window.width * (x / 100), self.window.height * (y / 100)
