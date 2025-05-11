from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')


from kivy.app import App
from kivy import platform
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10
    V_LINES_SPACING = .25  # percentage in screen width
    vertical_lines = []

    H_NB_LINES = 8
    H_LINES_SPACING = .15  # percentage in screen height
    horizontal_lines = []

    SPEED_Y = 2  # Vitesse verticale
    current_offset_y = 0

    SPEED_X = 12  # Vitesse horizontale
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.bind(size=self.on_size)

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False



    def on_size(self, *args):
        self.perspective_point_x = self.width / 2
        self.perspective_point_y = self.height * 0.75
        self.update_vertical_lines()
        self.update_horizontal_lines()

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5

        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line_x + offset * spacing + self.current_offset_x)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        if len(self.vertical_lines) > 0 and len(self.horizontal_lines) == self.H_NB_LINES:
            first_line_x = self.vertical_lines[0].points[0]
            last_line_x = self.vertical_lines[-1].points[0]

            spacing_y = self.H_LINES_SPACING * self.height
            for i in range(0, self.H_NB_LINES):
                line_y = i * spacing_y - self.current_offset_y

                # Gestion du débordement pour un défilement infini
                if line_y < 0:
                    line_y += spacing_y * self.H_NB_LINES

                x1, y1 = self.transform(first_line_x, line_y)
                x2, y2 = self.transform(last_line_x, line_y)
                self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        y_normalized = y / self.perspective_point_y
        if y_normalized > 1:
            y_normalized = 1

        perspective_factor = 1 - y_normalized
        offset_x = (x - self.perspective_point_x) * perspective_factor

        tr_x = self.perspective_point_x + offset_x
        tr_y = self.perspective_point_y * y_normalized

        return int(tr_x), int(tr_y)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = - self.SPEED_X
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True

    def on_touch_down(self, touch):
        if touch.x < self.width/2:
            print("<-")
            self.current_speed_x = self.SPEED_X
        else:
            print("->")
            self.current_speed_x = - self.SPEED_X


    def un_touch_up(self, touch):
        print("UP")
        self.current_speed_x = 0

    def update(self, dt):
        time_factor = dt * 60  # Normalisation pour 60 FPS

        # Mise à jour du déplacement vertical
        self.current_offset_y += self.SPEED_Y * time_factor
        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        # Mise à jour du déplacement horizontal
        self.current_offset_x += self.current_speed_x * time_factor
        spacing_x = self.V_LINES_SPACING * self.width
        if abs(self.current_offset_x) >= spacing_x:
            self.current_offset_x = 0

        self.update_vertical_lines()
        self.update_horizontal_lines()


class GalaxyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    GalaxyApp().run()