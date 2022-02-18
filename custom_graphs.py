import os
import sys
os.environ['KIVY_HOME'] = sys.path[0]

from kivy_garden.graph import Graph
import kivy.properties as kp
from custom_plots import CubicPlot
from kivy.uix.bubble import Bubble, BubbleContent
from kivy.uix.label import Label
from kivy.core.window import Window


class CursorDataPosBubble(Bubble):
    def __init__(self, pos, **kwargs):
        super().__init__(**kwargs)
        # values = ('left_top', 'left_mid', 'left_bottom', 'top_left',
        #           'top_mid', 'top_right', 'right_top', 'right_mid',
        #           'right_bottom', 'bottom_left', 'bottom_mid', 'bottom_right')
        # index = values.index(self.arrow_pos)
        # self.arrow_pos = values[(index + 1) % len(values)]
        pos = (round(pos[0], ndigits=2), round(pos[1], ndigits=2))
        self.add_widget(Label(text=f"{pos[0]}x{pos[1]}"))


class DesignGraph(Graph):
    xmax = kp.NumericProperty(22000)
    xmin = kp.NumericProperty(18)
    ymax = kp.NumericProperty(20)
    ymin = kp.NumericProperty(-20)
    xlog = kp.BooleanProperty(True)
    x_ticks_major = kp.NumericProperty(0.1)
    x_grid = kp.BooleanProperty(True)
    x_grid_label = kp.BooleanProperty(True)
    y_ticks_major = kp.NumericProperty(3)
    y_grid = kp.BooleanProperty(True)
    y_grid_label = kp.BooleanProperty(True)
    ylabel = kp.StringProperty('Amplitude (dB)')
    xlabel = kp.StringProperty('freq (Hz)')
    visual_mode = kp.BooleanProperty(False)
    cubic_plot = kp.ObjectProperty(None)
    prev_touch = kp.ObjectProperty(None, allownone=True)
    prev_x = kp.NumericProperty(-1)
    cursor_pos_bubble = kp.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cubic_plot = CubicPlot(self.xmin, self.xmax)
        self.add_plot(self.cubic_plot)
        self.add_plot(self.cubic_plot.get_inner_plot())
        Window.bind(mouse_pos=self.on_motion)

    def menu_was_clicked(self, x, y):
        from menus import MainMenu
        mainmenu = [m for m in self.walk() if issubclass(m.__class__, MainMenu)][0]
        for item in mainmenu.walk():
            try:
                submenu = item.get_submenu()
                if submenu.self_or_submenu_collide_with_point(x, y) is not None:
                    return True
            except: pass
        return False

    # pseudo działające zoomy
    def _zoom_in(self):
        if self.ymin < -15 and self.ymax > 15:
            if self.ymin < -24 and self.ymax > 24:
                self.ymin += 1
                self.ymax -= 1
            else:
                self.ymin += 3
                self.ymax -= 3

    def _zoom_out(self):
        if self.ymin > -99:
            self.ymin -= 3
            self.ymax += 3

    def on_touch_down(self, touch):
        if self.menu_was_clicked(*self.to_widget(touch.x, touch.y, True)):
            return True
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self._zoom_in()
            elif touch.button == 'scrollup':
                self._zoom_out()
            if self.ymax - self.ymin >= 90:
                self.y_ticks_major = int((self.ymax - self.ymin)/20)
            else:
                self.y_ticks_major = 3
            return True
        elif touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                if self.xmin >= 10  and self.xmax <= 22000:
                    self.xmin += 2
                    self.xmax -= 2
            elif touch.button == 'scrollup':
                if self.xmin <= 9000 and self.xmax >= 10000:
                    self.xmin += 2
                    self.xmax -= 2
            return True
        elif touch.button == 'left':
            touch.grab(self)
            return False
        elif touch.button == 'right':
            x, y = self.to_widget(touch.x, touch.y, True)
            self.cubic_plot.remove_point(self.to_data(x, y)[0])
            self.prev_x = self.to_data(x, y)[0]
            touch.grab(self)
            return False
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.menu_was_clicked(*self.to_widget(touch.x, touch.y, True)):
            return True
        if touch.button == 'left':
            touch.ungrab(self)
            x, y = self.to_widget(touch.x, touch.y, True)
            if self.collide_plot(x, y):
                x0, y0 = self.to_data(x, y)
                self.cubic_plot.add_point(int(x0), y0)
                return True
        elif touch.button == 'right':
            if self.prev_x != -1:
                x, _ = self.to_widget(touch.x, touch.y, True)
                x0, _ = self.to_data(x, _)
                start = min(int(self.prev_x), int(x0))
                stop = max(int(self.prev_x), int(x0))
                for x in range(start, stop):
                    self.cubic_plot.remove_point(x)
            touch.ungrab(self)
            self.prev_x = -1

        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.button == 'middle' and touch.grab_current is self and not self.visual_mode:
            return True
        if touch.button == 'left' and touch.grab_current is self and not self.visual_mode:
            x, y = self.to_widget(touch.x, touch.y, True)
            if self.collide_plot(x, y):
                x0, y0 = self.to_data(x,y)
                self.cubic_plot.add_point(x0, y0)
                # return True

    def on_motion(self, instance, value):
        if self.cursor_pos_bubble is not None:
            self.remove_widget(self.cursor_pos_bubble)
        x, y = self.to_widget(*value)
        pos = self.to_data(x, y)
        self.cursor_pos_bubble = CursorDataPosBubble(pos)
        self.add_widget(self.cursor_pos_bubble)
        pass

class VisualGraph(Graph):
    pass