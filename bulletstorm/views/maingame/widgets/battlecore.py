import imgui

from ....core.gui.widget import Widget

from ..battlecore.core import *
from ..battlecore.battlegame.actors import *


def make_player_party():
    player_party = Party("Player")
    player_party.add_actor(mitochondra_hero())
    return player_party


def make_enemy_party():
    enemy_party = Party("Enemy")
    enemy_party.add_actor(skeleton_enemy())
    return enemy_party


def init_battle():
    player_party = make_player_party()
    enemy_party = make_enemy_party()

    B = Battle()
    B.add_party(player_party)
    B.add_party(enemy_party)

    B.initialize()
    return B


class BattleCoreWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.last_output = ""
        self.battle_engine = BattleEngine()

        self._start_battle(init_battle())

        self.size = (256, 128), (-32, -32)

    def _start_battle(self, battle):
        self.battle_engine.battle = battle
        self.battle_engine._next_turn()

    def _battle_turn_ui(self):
        output = ""
        imgui.text(
            f"Turn: {self.battle_engine.battle.turn}\t{self.battle_engine.active_actor.name}'s turn"
        )
        if self.battle_engine.is_player_turn:
            for action in self.battle_engine.active_actor.actions:
                if action in self.battle_engine.active_actor.possible_actions:
                    if imgui.button(action.name):
                        targets = self.battle_engine._get_possible_action_targets(
                            action
                        )
                        if len(targets) == 1:
                            target = targets[0]
                        else:
                            imgui.text("Select target:")
                            for t in targets:
                                if imgui.button(t.name):
                                    target = t
                        self.battle_engine._do_action(action, target)
                        output = f"{self.battle_engine.active_actor.name} used {action.name} on {target.name}"
        else:
            if imgui.button("Next"):
                output = self.battle_engine._perform_bot_action()
        return output

    def draw(self):
        with imgui.begin("Battle UI"):
            if not self.battle_engine.battle.is_over:
                imgui.text(self.last_output)
                last_output = self._battle_turn_ui()
                if last_output:
                    self.last_output = last_output
                    self.battle_engine._next_turn()
                elif imgui.button("End Turn"):
                    self.battle_engine._next_turn()
            else:
                imgui.text("Battle over!")
                # imgui.text(f"Winner: {self.battle_engine.battle.winner.name}")
                if imgui.button("Restart"):
                    # does not work because hp is not saved between battles atm.
                    self._start_battle(init_battle())

        # imgui.text(f"\n{self.battle_engine.battle _stats.pretty_stats()}")
