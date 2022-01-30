""" Okno głowne programu,
składa sie z innych konkretnych okien ktorych wizualizacja jest stworzona
w innych plikach pythona.
"""
import os
import sys
import random
import math

from configs import *
from kivy_garden.graph import Graph, MeshLinePlot

os.environ['KIVY_HOME'] = sys.path[0]
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
from main_menu import MainMenu
from main_menu import FileMenu
import main_menu
from kivy.uix.widget import Widget
import kivy.properties as kp
from kivy.utils import colormap, get_color_from_hex
from kivy.graphics import *
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
kivy.require('2.0.0')


class CstWidget(ButtonBehavior, Widget):
    color = kp.ColorProperty("#ff1caa")

    def __init__(self, id, /, **kwargs):
        self.id = id
        if 'color' in kwargs:
            if isinstance(kwargs['color'], (tuple,list)): self.color = kwargs['color']
            elif isinstance(kwargs['color'], Color): self.color = kwargs['color'].rgb
            elif isinstance(kwargs['color'], str):
                try: self.color = get_color_from_hex(kwargs['color'])
                except:
                    try: self.color = get_color_from_hex(colormap[kwargs['color']])
                    except: raise ValueError("Color string can't be apply to property.")
            del kwargs['color']
        super().__init__(**kwargs)
        self.draw_button()

    def draw_button(self):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            Rectangle(size=self.size, pos=self.pos)
            Label(text=f'{self.id}', pos=self.pos, size=self.size)

    def redraw(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            Rectangle(size=self.size, pos=self.pos)
            Label(text=f'{self.id}', pos=self.pos, size=self.size)

    def on_press(self):
        r,g,b = [random.random() for _ in range(3)]
        _get = lambda x: math.ceil(x) if x > 0.5 else math.floor(x)
        self.color = [_get(r), _get(g), _get(b)]

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         r,g,b = [random.random() for x in range(3)]
    #         _get = lambda x: math.ceil(x) if x>0.5 else math.floor(x)
    #         self.color = [_get(r), _get(g), _get(b)]
    #     return False

    def on_color(self, instance, value):
        self.draw_button()
        self.canvas.ask_update()


class MainLayout(FloatLayout):

    main_menu_layout = kp.ObjectProperty(None)

    def on_size(self, inst, val):
        try:
            self.size_hint = (1, self.window.height - self.mmr.height)
        except AttributeError:
            try:
                self.size_hint = (1, self.window.size[1] - self.mmr.height)
            except:
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
        self.main_options = MainOptions()
        self.design_options = DesignOptions()
        self.visual_options = VisualizationOptions()
        box_layout = BoxLayout(size=Window.size, orientation='vertical')
        main_layout = FloatLayout(size=Window.size)
        # main_layout.bind(size=self.resize)
        with main_layout.canvas:
            Color(0,0,1,0.2)
            Rectangle(size=main_layout.size, pos=main_layout.pos)

        layout = FloatLayout(size_hint=(1, 1), size=(20, 20))
        # alayout = AnchorLayout(anchor_x='left', anchor_y='top', padding=(5, 6, 5, 6), size_hint=(1, 1))
        button = CstWidget('Od trzech tygodni', color=[0.6, 0, 0], size=(200, 50), pos=(200, 50),
                           size_hint=(None, None))
        button2 = CstWidget('Jurku', color=(0, 0, 1), size=(100, 30), pos=(100, 150), size_hint=(0.2, 0.2))
        # mm = MainMenu(self.main_options, self.design_options, self.visual_options, cancel_handler_widget=layout)
        mm = Builder.load_file("main_menu.kv")
        operation_layout = Builder.load_file("main_window.kv")
        operation_layout.set_references(mm, Window)
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, math.sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        button2.bind(size=button2.redraw)
        layout.add_widget(button2)
        layout.add_widget(button)
        layout.add_widget(graph)
        # box_layout.add_widget(alayout)
        main_layout.add_widget(operation_layout)
        main_layout.add_widget(mm) # main menu dodać jako ostatnie

        return main_layout


if __name__ == '__main__':
    MainWindow().run()