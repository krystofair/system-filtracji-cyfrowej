""" Okno głowne programu,
składa sie z innych konkretnych okien ktorych wizualizacja jest stworzona
w innych plikach pythona.
"""
import os
import sys
import random
import math
os.environ['KIVY_HOME'] = sys.path[0]

from configs import *
from kivy_garden.graph import Graph, MeshLinePlot, Plot


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
from kivy.core.window import Window
from main_menu import *
import main_menu
from kivy.uix.widget import Widget
import kivy.properties as kp
from kivy.utils import colormap, get_color_from_hex
from kivy.graphics import *
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
kivy.require('2.0.0')

from scipy.interpolate import CubicSpline

from custom_plots import CubicPlot


class MyGraph(Graph):
    xmax_const = 22000
    xmin_const = 18
    data_points = kp.DictProperty()
    visual_mode = kp.BooleanProperty(False)
    mlp = kp.ObjectProperty(MeshLinePlot(mode='line-strip'))


    def on_touch_down(self, touch):
        if touch.button == 'left':
            touch.grab(self)
            return False
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.button == 'left':
            touch.ungrab(self)
            x, y = self.to_widget(touch.x, touch.y, True)
            if self.collide_plot(x, y):
                x0, y0 = self.to_data(x, y)
                self.data_points.update({int(x0): round(y0, ndigits=2)})
                return True
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self and not self.visual_mode:
            x, y = self.to_widget(touch.x, touch.y, True)
            if self.collide_plot(x, y):
                x0, y0 = self.to_data(x,y)
                self.data_points.update({int(x0):round(y0, ndigits=2)})
                # return True
        return super().on_touch_move(touch)

    def on_data_points(self, i, v):
        print(list(v.items())[len(v)-1])
        self.mlp.points = self.data_points.items()
        self.mlp.points.sort()
        if len(self.plots) < 1:
            self.add_plot(self.mlp)
        self.mlp.plot_mesh()


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

        # graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        #               x_ticks_major=25, y_ticks_major=1,
        #               y_grid_label=True, x_grid_label=True, padding=5,
        #               x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        # graph.add_plot(plot)
        # layout.add_widget(graph)
        # main_layout.add_widget(mm) # main menu dodać jako ostatnie

        return main_wnd_view


if __name__ == '__main__':
    MainWindow().run()