import arcade
import arcade.gui
import logging

from .gui.view import GuiView

logger = logging.getLogger(__name__)


def reset_player(window):
    player = window.pages["primary"].player
    player.center_x = window.width / 2
    player.center_y = window.height / 2
    player.reset()

    window.show_view("primary")


class GameOverView(GuiView):
    def __init__(self, window):
        super().__init__(window, "gameover", "Game Over")

        self.uimanager = arcade.gui.UIManager(self.window)
        continue_prompt = arcade.gui.UITextArea(
            text="Continue?",
            font_size=20,
            center_x=400,
            center_y=400,
            color=arcade.color.WHITE,
        )
        continue_prompt = arcade.gui.UIAnchorWidget(child=continue_prompt)
        button_layout = arcade.gui.UIBoxLayout(vertical=False)
        yes_button = arcade.gui.UIFlatButton(text="Yes", center_x=400, center_y=225)
        yes_button.on_click = lambda _: reset_player(self.window)
        # yes_button = arcade.gui.UIAnchorWidget(
        #     child=yes_button, anchor_x="center", anchor_y="center"
        # )
        no_button = arcade.gui.UIFlatButton(text="No", center_x=400, center_y=200)
        no_button.on_click = lambda _: self.window.pages["primary"].restart_game()
        # no_button = arcade.gui.UIAnchorWidget(
        #     child=no_button, anchor_x="center", anchor_y="center"
        # )

        layout = arcade.gui.UIBoxLayout()
        layout.add(continue_prompt)
        layout.add(no_button)
        layout.add(yes_button)

        #   layout.add(button_layout)
        layout = arcade.gui.UIAnchorWidget(
            child=layout, anchor_x="center", anchor_y="center"
        )

        self.uimanager.add(layout)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.uimanager.enable()

    def on_hide_view(self):
        self.uimanager.disable()
        return super().on_hide_view()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over!\t:(", 50, 50, arcade.color.RED, 50)
        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        logger.debug("Restarting game...")
        self.window.views["primary"].restart_game()
