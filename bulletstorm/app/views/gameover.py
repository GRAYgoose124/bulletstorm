import arcade
import arcade.gui
import logging


logger = logging.getLogger(__name__)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager(self.window)
        continue_prompt = arcade.gui.UITextArea(
            text="Continue?", font_size=20, center_x=400, center_y=400, color=arcade.color.WHITE)
        yes_button = arcade.gui.UIFlatButton(
            text="Yes", center_x=400, center_y=300)
        no_button = arcade.gui.UIFlatButton(
            text="No", center_x=400, center_y=200)

        continue_prompt = arcade.gui.UIAnchorWidget(child=continue_prompt)
        yes_button = arcade.gui.UIAnchorWidget(
            child=yes_button, anchor_x="center", anchor_y="center")
        no_button = arcade.gui.UIAnchorWidget(
            child=no_button, anchor_x="center", anchor_y="center")

        layout = arcade.gui.UIBoxLayout()
        layout.add(continue_prompt)
        button_layout = arcade.gui.UIBoxLayout(vertical=False)
        button_layout.add(yes_button)
        button_layout.add(no_button)
        layout.add(button_layout)

        self.manager.add(layout)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over!\t:(", 50, 50, arcade.color.RED, 50)
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        logger.debug("Restarting game...")
        self.window.views["primary"].restart_game()
        self.window.show_view("primary")
