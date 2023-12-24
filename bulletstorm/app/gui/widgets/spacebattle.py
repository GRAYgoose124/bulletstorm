import imgui
import imgui.core

from .core import Widget


class ShipUiWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(-32, -32, widget_size=widget_size), imgui.ONCE
        )

        with imgui.begin("Ship UI"):
            if imgui.button("Fire Missile"):
                self.button_message = "You fired a missile!"
            if imgui.button("Speak to Ship AI"):
                self.button_message = "Biya! Biya!"
            imgui.text(self.button_message)
            imgui.text(f"Health: {self.page.player.hp}")


from ....battlecore.core import *
from ....battlecore.game.actors import *


class BattleCoreWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.battle_message = ""
        self.battle_engine = BattleEngine()

        player_party = Party("Player")
        player_party.add_actor(mitochondra_hero)

        enemy_party = Party("Enemy")
        enemy_party.add_actor(skeleton_enemy)

        B = Battle()
        B.add_party(player_party)
        B.add_party(enemy_party)
        self.battle_engine.set_battle(B)
        self.battle_engine.battle.initialize()
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
                        self.battle_engine._next_turn()
                        output = f"{self.battle_engine.active_actor.name} used {action.name} on {target.name}"
                if imgui.button("End Turn"):
                    self.battle_engine._next_turn()
        else:
            if imgui.button("Next"):
                output = self.battle_engine._perform_bot_action(end_turn=True)
        return output

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(512, 512, widget_size=widget_size), imgui.ONCE
        )

        last_output = ""
        with imgui.begin("Battle UI"):
            if not self.battle_engine.battle.is_over:
                imgui.text(last_output)
                last_output = self._battle_turn_ui()
            else:
                imgui.text("Battle over!")
                # imgui.text(f"Winner: {self.battle_engine.battle.winner.name}")
                if imgui.button("Restart"):
                    # does not work because hp is not saved between battles atm.
                    self.battle_engine.battle.initialize()
                    self.battle_engine._next_turn()
        # imgui.text(f"\n{self.battle_engine.battle _stats.pretty_stats()}")
