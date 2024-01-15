import imgui


class Widget:
    def __init__(self, guiview, draw_mode=imgui.ALWAYS):
        self.page = guiview
        self.draw_mode = draw_mode

    def draw(self):
        raise NotImplementedError
