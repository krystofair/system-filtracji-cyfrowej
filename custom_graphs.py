#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from kivy.app import App
from kivy_garden.graph import Graph
import kivy.properties as kp
from custom_plots import DesignPlot
import store


class DesignGraph(Graph):
    xmax = kp.NumericProperty(20000)
    xmin = kp.NumericProperty(20)
    ymax = kp.NumericProperty(12)
    ymin = kp.NumericProperty(-12)
    xlog = kp.BooleanProperty(False)
    x_ticks_major = kp.NumericProperty(500)
    x_grid = kp.BooleanProperty(True)
    x_grid_label = kp.BooleanProperty(True)
    y_ticks_major = kp.NumericProperty(3)
    y_grid = kp.BooleanProperty(True)
    y_grid_label = kp.BooleanProperty(True)
    ylabel = kp.StringProperty('Amplitude (dB)')
    xlabel = kp.StringProperty('frequency (Hz)')
    design_plot = kp.ObjectProperty(None)
    prev_touch = kp.ObjectProperty(None, allownone=True)
    prev_x = kp.NumericProperty(-1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.design_plot = DesignPlot(self.xmin, self.xmax)
        self.add_plot(self.design_plot)
        self.add_plot(self.design_plot.get_inner_plot())
        # Window.bind(mouse_pos=self.on_motion)

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
        if App.get_running_app().menus[0].collide_point(*self.to_widget(touch.x, touch.y, True)):
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
            self.design_plot.remove_point(self.to_data(x, y)[0])
            self.prev_x = self.to_data(x, y)[0]
            touch.grab(self)
            return False
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if App.get_running_app().menus[0].collide_point(*self.to_widget(touch.x, touch.y, True)):
            return True
        if touch.button == 'left':
            touch.ungrab(self)
            x, y = self.to_widget(touch.x, touch.y, True)
            if self.collide_plot(x, y):
                x0, y0 = self.to_data(x, y)
                self.design_plot.add_point(int(x0), y0)
                # current_filter = store.get('loaded-filter')
                # if current_filter:
                #     store.update(f'{current_filter}-generated', False)
                return True
        elif touch.button == 'right':
            if self.prev_x != -1:
                x, _ = self.to_widget(touch.x, touch.y, True)
                x0, _ = self.to_data(x, _)
                start = min(int(self.prev_x), int(x0))
                stop = max(int(self.prev_x), int(x0))
                for x in range(start, stop):
                    self.design_plot.remove_point(x)
            touch.ungrab(self)
            self.prev_x = -1

        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.button == 'middle' and touch.grab_current is self:
            return True
        if touch.button == 'left' and touch.grab_current is self:
            x, y = self.to_widget(touch.x, touch.y, True)
            if self.collide_plot(x, y):
                x0, y0 = self.to_data(x, y)
                self.design_plot.add_point(x0, y0)
                # return True


class VisualGraph(Graph):
    xmax = kp.NumericProperty(20000)
    xmin = kp.NumericProperty(20)
    ymax = kp.NumericProperty(18)
    ymin = kp.NumericProperty(-18)
    ylabel = kp.StringProperty('Amplitude (dB)')
    xlabel = kp.StringProperty('freq (Hz)')
    xlog=kp.BooleanProperty(False)
    x_grid = kp.BooleanProperty(True)
    x_grid_label = kp.BooleanProperty(True)
    y_grid = kp.BooleanProperty(True)
    y_grid_label = kp.BooleanProperty(True)
    y_ticks_major = kp.NumericProperty(3)
    x_ticks_major = kp.NumericProperty(500)
    # precision = kp.NumericProperty(2)

    def on_update(self):
        """
        Call this when you load new samples to buffer in order to show.
        Or find another way i.e binding like in interpolation from design graph.
        """
        pass

    def load_origins(self, samples):
        pass

    def load_filtered(self, samples):
        # TODO: Question if that method is necesarry?
        # Whether the graph will be executing filtering for itself?
        pass

