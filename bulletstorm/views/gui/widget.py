class Widget:
    def __init__(self, guiview):
        self.page = guiview

    def draw(self):
        raise NotImplementedError
