import time, logging

log = logging.getLogger(__name__)


class LevelViewMixin:
    def __init__(self, level_cls=None):
        self.level = None
        self.level_constructor = level_cls

        self._game_over = False
        self._restart = False

        self.player = None
        self.player_controls_str = ""

    def init_level(self):
        self._game_over = False
        self._restart = False

        assert self.level_constructor is not None
        self.level = self.level_constructor(self)
        self.player = self.level.player

        assert self.player is not None
        self.player_controls_str = "\n".join(
            f"{control}: {key}" for control, key in self.player.keybinds
        )

        log.info(f"Initialized level {self.level_constructor.__name__}")
        log.info(f"Player: {self.player}")

    def select_level(self, level_cls):
        self.level_constructor = level_cls
        self.init_level()

    def update(self, delta_time):
        self.level.update(delta_time)

    def restart_game(self):
        self._restart = True
        self.end_game()

    def end_game(self):
        self._game_over = time.time()

    def on_resize(self, width: int, height: int):
        self.level.resize(width, height)
