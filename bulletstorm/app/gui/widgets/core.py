class Widget:
    def __init__(self, gui):
        self.gui = gui

    def draw(self):
        raise NotImplementedError
