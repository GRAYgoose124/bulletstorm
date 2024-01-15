class LevelBase:
    def __init__(self, parent):
        self.parent = parent

        self._player = None
        self.manager = None

        self.size = None
        self.resize(*self.parent.window.get_size())
        self.setup()

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value
        self.parent.player = value

    def setup(self):
        raise NotImplementedError

    def update_level(self, delta_time):
        pass

    def resize(self, width, height):
        self.size = (width, height)
        # self.setup()

    def update(self, delta_time: float):
        self.update_level(delta_time)

        # run the physics update
        self.manager.step(delta_time)

        # check if player is dead
        if self.player.hp <= 0:
            self.parent.end_game()

    def draw(self):
        self.manager.draw()
