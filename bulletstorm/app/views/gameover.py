import arcade


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 300, 300, arcade.color.WHITE, 54)

    def on_key_press(self, key, modifiers):
        self.window.show_view("primary")