import arcade
import arcade.gui


class PauseView(arcade.View):
    def __init__(self):
        super().__init__()

        self.uimanager = arcade.gui.UIManager()

        self._pause_screen = self.__build_pause_screen()
        self._settings_menu = self.__build_settings_menu()
        self._exit_dialog_handle = None

        self.uimanager.add(arcade.gui.UIAnchorWidget(
            child=self._pause_screen, anchor_x="center", anchor_y="center"))

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.uimanager.enable()

    def on_hide_view(self):
        self.uimanager.disable()
        return super().on_hide_view()

    def on_draw(self):
        arcade.start_render()
        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.uimanager.remove(self._exit_dialog_handle)

            self._exit_dialog_handle = arcade.gui.UIMessageBox(width=300, height=150, message_text="Are you sure you want to quit?",
                                                               buttons=("Ok", "Cancel"))

            self._exit_dialog_handle._callback = self.__exit_game_dialog

            self.uimanager.add(self._exit_dialog_handle)

        return super().on_key_press(key, modifiers)

    # UI building
    def __build_pause_screen(self):
        pause_screen = arcade.gui.UIBoxLayout()

        pause_title = arcade.gui.UITextArea(
            text="Paused", font_size=20, font_name="Arial", color=arcade.color.GRAY_BLUE)

        pause_buttons = arcade.gui.UIBoxLayout()
        resume_button = arcade.gui.UIFlatButton(
            text="Resume", width=200, height=50)
        resume_button.on_click = self.__resume_game
        resume_button = arcade.gui.UIAnchorWidget(
            child=resume_button, anchor_x="center", anchor_y="center")

        settings_button = arcade.gui.UIFlatButton(
            text="Settings", width=200, height=50)
        settings_button.on_click = lambda _: self.uimanager.add(
            self._settings_menu)
        settings_button = arcade.gui.UIAnchorWidget(
            child=settings_button, anchor_x="center", anchor_y="center", align_y=-55)

        quit_button = arcade.gui.UIFlatButton(
            text="Quit", width=200, height=50)
        quit_button.on_click = lambda _: arcade.close_window()
        quit_button = arcade.gui.UIAnchorWidget(
            child=quit_button, anchor_x="center", anchor_y="center", align_y=-110)

        pause_buttons.add(resume_button)
        pause_buttons.add(settings_button)
        pause_buttons.add(quit_button)

        # build screen
        pause_screen.add(arcade.gui.UIAnchorWidget(
            child=pause_title, align_x=150, anchor_y="top"))
        pause_screen.add(arcade.gui.UIAnchorWidget(
            child=pause_buttons, anchor_x="center", anchor_y="center"))

        return pause_screen

    def __build_settings_menu(self):
        menu = arcade.gui.UIBoxLayout()
        menu.add(arcade.gui.UITextArea(text="Settings", font_size=20,
                 font_name="Arial", color=arcade.color.WHITE))

        # settings menu close button
        close_button = arcade.gui.UIFlatButton(
            text="Close", width=200, height=50)
        close_button.on_click = lambda _: self.uimanager.remove(menu)

        menu.add(arcade.gui.UIAnchorWidget(
            child=close_button, anchor_x="center", anchor_y="right"))

        return menu

    # UI callbacks
    def __resume_game(self, event):
        self.uimanager.remove(self._settings_menu)

        self.window.show_view("primary")

    def __exit_game_dialog(self, button_text):
        if button_text == "Ok":
            arcade.close_window()
