import os
import sys
os.environ['KIVY_HOME'] = sys.path[0]

from kivy_garden.graph import Graph
import kivy.properties as kp
from custom_plots import CubicPlot


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
    ctrl_is_pressed = kp.BooleanProperty(False)
    shift_is_pressed = kp.BooleanProperty(False)
    prev_touch = kp.ObjectProperty(None, allownone=True)
    prev_x = kp.NumericProperty(-1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cubic_plot = CubicPlot(self.xmin, self.xmax)
        self.add_plot(self.cubic_plot)
        self.add_plot(self.cubic_plot.get_inner_plot())

    def on_parent(self, widget, parent):
        self.focus = True

    def on_key_down(self, keycode, text, modifiers):
        print('key is down')
        if keycode == self.keycodes['rctrl'] or keycode == self.keycodes['lctrl']:
            self.ctrl_is_pressed = True
        return super().on_key_down(keycode, text, modifiers)

    def on_key_up(self, keycode):
        if keycode == self.keycodes['rctrl'] or keycode == self.keycodes['lctrl']:
            self.ctrl_is_pressed = False
        return super().on_key_up(keycode)

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
        if touch.is_mouse_scrolling and not self.ctrl_is_pressed:
            if touch.button == 'scrolldown':
                self._zoom_in()
            elif touch.button == 'scrollup':
                self._zoom_out()
            if self.ymax - self.ymin >= 90:
                self.y_ticks_major = int((self.ymax - self.ymin)/20)
            else:
                self.y_ticks_major = 3
            return True
        elif touch.is_mouse_scrolling and self.ctrl_is_pressed:
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
            self.prev_x = self.to_data(x,y)[0]
            touch.grab(self)
            return False
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
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
        return super().on_touch_move(touch)


class VisualGraph(Graph):
    pass