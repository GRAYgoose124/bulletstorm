import time
import arcade


class Player:
    DEFAULT_CONTROL_CONFIG = {
        "PLAYER_FORWARD_ACCELERATION": 1,
        "PLAYER_LATERAL_ACCELERATION": 1,
        "PLAYER_TURN_VELOCITY": 0.035
    }

    DEFAULT_KEYBINDS = {
        "PLAYER_MOVE_FORWARD": arcade.key.W,
        "PLAYER_MOVE_BACKWARD": arcade.key.S,
        "PLAYER_MOVE_LEFT": arcade.key.A,
        "PLAYER_MOVE_RIGHT": arcade.key.D,

        "PLAYER_TURN_LEFT": arcade.key.Q,
        "PLAYER_TURN_RIGHT": arcade.key.E,

        "PLAYER_SHOOT": arcade.key.SPACE,

        "PAUSE_MENU": arcade.key.ESCAPE
    }

    def __init__(self):
        self.sprite = None

        self.hp = 100
        self.last_hit = None

        self.acceleration = [0, 0]
        self.rotation = 0

        self.is_firing = False

        self._settings = {
            "keybinds": self.DEFAULT_KEYBINDS,
            "keybind_settings": self.DEFAULT_CONTROL_CONFIG
        }

    @property
    def settings(self):
        return self._settings

    @property
    def keybind_settings(self):
        return self._settings['keybind_settings']

    @property
    def keybinds(self):
        return self._settings['keybinds']

    def reset(self):
        self.hp = 100
        self.last_hit = None

        self.acceleration = [0, 0]
        self.rotation = 0

        self.is_firing = False

    def take_damage(self, damage=1, cooldown=1.0):
        t = time.time()
        if self.last_hit is None or t - self.last_hit > cooldown:
            self.hp -= damage
            self.last_hit = t
