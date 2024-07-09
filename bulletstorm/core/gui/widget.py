import imgui


class Widget:
    def __init__(self, guiview, draw_mode=imgui.ALWAYS, size=(32, 32), pos=(0, 0)):
        self.page = guiview
        self.draw_mode = draw_mode
        self.size = size, pos

    def draw(self):
        raise NotImplementedError
