import imgui
import imgui.core

from .core import Widget


class ButtonTestWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(-32, -32, widget_size=widget_size), imgui.ONCE
        )

        with imgui.begin("Widget: Button Test"):
            if imgui.button("Button 1"):
                self.button_message = "You pressed 1!"
            if imgui.button("Button 2"):
                self.button_message = "You pressed 2!"
            imgui.text(self.button_message)
            imgui.text(f"Health: {self.page.player.hp}")


from ....battlecore.core import *
from ....battlecore.game.actors import *


class BattleCoreWidget(Widget):
    def __init__(self, page):
        super().__init__(page)

        self.button_message = ""
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

    def draw(self):
        widget_size = self.page.percent_of(0.25, 0.25)
        imgui.set_next_window_size(*widget_size, imgui.ONCE)
        imgui.set_next_window_position(
            *self.page.rel_to_window(512, 512, widget_size=widget_size), imgui.ONCE
        )

        with imgui.begin("Battle Core"):
            # if active actor is Plaer party
            if self.battle_engine.is_player_turn:
                imgui.text("Player turn")
                for action in self.battle_engine.active_actor.actions:
                    if action in self.battle_engine.active_actor.possible_actions:
                        if imgui.button(action.name):
                            targets = self.battle_engine._get_possible_action_targets(
                                action
                            )
                            if len(targets) == 1:
                                self.battle_engine._do_action(action, targets[0])
                            else:
                                imgui.text("Select target:")
                                for target in targets:
                                    if imgui.button(target.name):
                                        self.battle_engine._do_action(action, target)
                    if imgui.button("End Turn"):
                        self.battle_engine._next_turn()

            else:
                imgui.text("Enemy turn")
                if imgui.button("Next"):
                    self.battle_engine._perform_bot_action(end_turn=True)
