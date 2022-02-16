""" Okno głowne programu,
składa sie z innych konkretnych okien ktorych wizualizacja jest stworzona
w innych plikach pythona.
"""
import os
import sys
import math
os.environ['KIVY_HOME'] = sys.path[0]


from configs import *
from kivy_garden.graph import Graph


import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy_garden.contextmenu import *
from kivy.core.window import Window, WindowBase
from main_menu import *
import main_menu
from kivy.uix.widget import Widget
import kivy.properties as kp
from kivy.core.window import Keyboard
from kivy.utils import colormap, get_color_from_hex
from kivy.graphics import *
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.relativelayout import RelativeLayout
kivy.require('2.0.0')

from custom_plots import CubicPlot

import numpy


class MyGraph(Graph):
    xmax = kp.NumericProperty(22000)
    xmin = kp.NumericProperty(18)
    ymax = kp.NumericProperty(20)
    ymin = kp.NumericProperty(-20)
    x_grid = kp.BooleanProperty(True)
    x_grid_label = kp.BooleanProperty(True)
    y_ticks_major = kp.NumericProperty(3)
    # data_points = kp.DictProperty()
    visual_mode = kp.BooleanProperty(False)
    # mlp = kp.ObjectProperty(MeshLinePlot(mode='line-strip'))
    # PtsPlot = kp.ObjectProperty(ScatterPlot(color=[0,0.4,1,0.7], point_size=5))
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
                for x in range(int(self.prev_x), int(x0)):
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

    def _avg_plot_values(self, iterable):
        for i, v in enumerate(iterable[1:]):
            i += 1
            if math.fabs(iterable[i-1] - v): pass



class AppMenuFLayout(FloatLayout): pass



class MainLayout(FloatLayout):
    pass


class MainWindow(App):
    _log_counter = 0

    @classmethod
    @property
    def log_counter(cls):
        cls._log_counter += 1
        return cls._log_counter

    @classmethod
    def MWLog(cls, text):
        print(cls.log_counter, text)

    @staticmethod
    def resize(obj, value):
        MainWindow.MWLog(f"resize called: new window value = {value}")
        obj.size = Window.size

    def build(self):
        # utworzenie obiektów opcji w klasie głównej programu
        mm = Builder.load_file("main_menu.kv")
        main_wnd_view = Builder.load_file("main_window.kv")
        main_wnd_view.add_widget(mm)
        self.main_options = mm.ids['app_menu'].m_opts
        self.design_options = mm.ids['app_menu'].d_opts
        self.visual_options = mm.ids['app_menu'].v_opts
        # main_layout = FloatLayout(size=Window.size)
        # main_layout.bind(size=self.resize)
        # with main_layout.canvas:
        #     Color(0,0,1,0.2)
        #     Rectangle(size=main_layout.size, pos=main_layout.pos)

        layout = FloatLayout(size_hint=(1, 1), size=(20, 20))
        # mm = MainMenu(self.main_options, self.design_options, self.visual_options, cancel_handler_widget=layout)
        # main_layout.add_widget(mm) # main menu dodać jako ostatnie

        return main_wnd_view


if __name__ == '__main__':
    MainWindow().run()