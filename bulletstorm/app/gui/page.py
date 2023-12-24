# MIT License
#
# Copyright (c) 2020 Kurtis Fields
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  https://github.com/kfields/arcade-imgui/blob/master/imdemo/imdemo/page.py
#
import arcade
import imgui
import imgui.core


class Page(arcade.View):
    def __init__(self, window, name, title):
        super().__init__(window)
        self.name = name
        self.title = title
        self.show_gui = True
        self.widgets = []

    def reset(self):
        pass

    def add_widget(self, widget_cls):
        self.widgets.append(widget_cls(self))

    @classmethod
    def create(self, app, name, title):
        page = self(app, name, title)
        page.reset()
        return page

    def on_draw(self):
        arcade.start_render()
        self.game_draw()

        if self.show_gui:
            imgui.new_frame()

            self.draw_mainmenu()
            self.draw_navbar()

            self._widget_draw()
            self.gui_draw()

            imgui.end_frame()

    def on_update(self, delta_time: float):
        return self.update(delta_time)

    def draw_navbar(self):
        imgui.set_next_window_position(16, 32, imgui.ONCE)
        imgui.set_next_window_size(256, 732, imgui.ONCE)

        with imgui.begin("Examples"):
            imgui.text("Hello, world!")

    def on_show_view(self):
        self.show_gui = True
        return super().on_show_view()

    def on_hide_view(self):
        self.show_gui = False
        imgui.new_frame()
        imgui.end_frame()
        return super().on_hide_view()

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            # View
            if imgui.begin_menu("View", True):
                clicked_metrics, self.window.view_metrics = imgui.menu_item(
                    "Metrics", "Cmd+M", self.window.view_metrics, True
                )

                imgui.end_menu()

            imgui.end_main_menu_bar()

    def game_draw(self):
        pass

    def gui_draw(self):
        pass

    def _widget_draw(self):
        for widget in self.widgets:
            widget.draw()

    def update(self, delta_time):
        pass

    def rel_to_mouse(self, x, y):
        pos = imgui.get_cursor_screen_pos()
        x1 = pos[0] + x
        y1 = pos[1] + y
        return x1, y1

    def rel_to_window(self, x, y, widget_size=None):
        """positives are from zero, negatives are from end of window"""

        if x < 0:
            if widget_size is not None:
                x -= widget_size[0]
            x = self.window.width + x
        if y < 0:
            if widget_size is not None:
                y -= widget_size[1]
            y = self.window.height + y

        return x, y

    def percent_of(self, x, y):
        """Converts percentage of window to window coordinates

        Args:
            x (int): percentage of window width
            y (int): percentage of window height
        """
        return self.window.width * x, self.window.height * y
