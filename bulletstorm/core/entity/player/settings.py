from dataclasses import dataclass

import arcade


def arcade_key_map(v, no_mods=True):
    for k, v2 in filter(
        lambda e: not e[0].startswith("_") and not e[0].startswith("MOD_"),
        arcade.key.__dict__.items(),
    ):
        if v == v2:
            return k


class PlayerConfig:
    pass


class PlayerKeybinds:
    def __iter__(self):
        # map control codes to their names (MOVE_FORWARD, int) -> (MOVE_FORWARD, "W")
        for control, code in filter(
            lambda e: not e[0].startswith("_"), self.__dict__.items()
        ):
            yield control, arcade_key_map(code)


class PlayerSettings(dict):
    def __init__(self, config, keybinds):
        self.config = config
        self.keybinds = keybinds
