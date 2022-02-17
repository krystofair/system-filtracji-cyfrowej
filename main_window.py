""" Okno głowne programu,
składa sie z innych konkretnych okien ktorych wizualizacja jest stworzona
w innych plikach pythona.
"""

import os
import sys
os.environ['KIVY_HOME'] = sys.path[0]

import configs
from custom_graphs import DesignGraph, VisualGraph
from menus import *

import kivy
from kivy.app import App
from kivy_garden.contextmenu import AppMenuTextItem
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
import kivy.properties as kp
kivy.require('2.0.0')


class AppMenuFLayout(FloatLayout): pass


class MainLayout(FloatLayout):
    pass


class MainWindow(App):
    design_graph = kp.ObjectProperty(DesignGraph())
    graph = kp.ObjectProperty()
    main_menu = kp.ObjectProperty()
    dynamic_menu_item = kp.ObjectProperty()
    main_options = kp.ObjectProperty(configs.MainOptions())
    design_options = kp.ObjectProperty(configs.DesignOptions())
    visual_options = kp.ObjectProperty(configs.VisualizationOptions())

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # self.graph = self.design_graph
    #     pass

    def _del_last_dynamic_menu(self):
        if self.dynamic_menu is not None:
            try:
                del self.dynamic_menu
                self.dynamic_menu = None
            except Exception as e: print(e)

    def set_visual_graph(self):
        self.graph = VisualGraph()

    def set_design_graph(self):
        self.graph = DesignGraph()

    def set_design_menu(self, instance):
        self._del_last_dynamic_menu()
        amti = AppMenuTextItem(text="Design Options")
        dsm = Builder.load_file('design_submenu.kv')
        amti.add_widget(dsm)
        self.dynamic_menu_item = amti
        instance.parent.main_menu.add_widget(amti)

    def set_visual_menu(self, instance):
        self._del_last_dynamic_menu()
        vsm = Builder.load_file('visual_submenu.kv')
        amti = AppMenuTextItem(text="Visual Options")
        amti.add_widget(vsm)
        self.dynamic_menu_item = amti
        instance.parent.main_menu.add_widget(amti)

    def build(self):
        Config.set('input', 'mouse', 'mouse, disable_multitouch')
        Config.write()
        # utworzenie obiektów opcji w klasie głównej programu
        # mm = Builder.load_file("main_menu.kv")
        main_wnd_view = Builder.load_file("main_window.kv")
        self.graph = DesignGraph()
        main_wnd_view.ids['place_for_graph'].add_widget(self.graph)
        # main_wnd_view.add_widget(mm)

        return main_wnd_view


if __name__ == '__main__':
    MainWindow().run()