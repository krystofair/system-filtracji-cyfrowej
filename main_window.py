""" Okno głowne programu,
składa sie z innych konkretnych okien ktorych wizualizacja jest stworzona
w innych plikach pythona.
"""
import os, sys
import random
import math

os.environ['KIVY_HOME'] = sys.path[0]

from configs import *

import kivy
from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy_garden.contextmenu import *
from kivy.core.window import Window
from main_menu import MainMenu
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
        self.canvas.clear()
        self.draw_button()
        self.canvas.ask_update()


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
        for child in obj.children[:]:
            if issubclass(type(child), Layout):
                child.size = value



    def build(self):
        # utworzenie obiektów opcji w klasie głównej programu
        self.main_options = MainOptions()
        self.design_options = DesignOptions()
        self.visual_options = VisualizationOptions()
        box_layout = BoxLayout(size=Window.size)
        box_layout.bind(size=MainWindow.resize)
        layout = FloatLayout()
        rlayout = RelativeLayout(pos=(300,300))
        button = CstWidget('dlaczego', color=[0.6, 0, 0], size=(200, 50), pos=(200, 50),
                           size_hint=(None, None))
        button2 = CstWidget('liczba? niewiem', color=(0, 0, 1), size=(100, 30), pos=(100, 150), size_hint=(None, None))
        button3 = CstWidget('kurwa ta', color=(0, 0, 1), size=(100, 30), pos=(100, 150), size_hint=(None, None))
        rlayout.add_widget(button3)
        layout.add_widget(rlayout)
        layout.add_widget(button2)
        layout.add_widget(button)
        box_layout.add_widget(layout)
        print(f'rozmiar układu typu box = {box_layout.size}')
        return box_layout


if __name__ == "__main__":
    MainWindow().run()
