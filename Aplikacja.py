# imports os, for config kivy
import os, sys
os.environ['KIVY_HOME'] = sys.path[0]
# os.environ['KIVY_NO_CONSOLELOG'] = '1';

# imports kivy
import kivy
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.app import App
from kivy.utils import interpolate
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

from math import sin
from kivy_garden.graph import Graph, MeshLinePlot

from kivy.lang import Builder

# imports kivy_garden
from libs.garden.contextmenu import AppMenu, AppMenuTextItem
# wymagana wersja frameworka kivy
kivy.require('2.0.0')

# other imports
# from scipy import interpolate



# class Aplikacji(App): pass
class KlasaAplikacji(App):
    def build(self):
        builder = Builder.load_string(KIVY_LAYOUT_STRING)
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        builder.add_widget(graph)
        return graph



if __name__ == '__main__':
    KlasaAplikacji().run()