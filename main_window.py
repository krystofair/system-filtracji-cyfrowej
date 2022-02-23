""" Okno głowne programu,
składa sie z innych konkretnych okien ktorych wizualizacja jest stworzona
w innych plikach pythona.
"""

import os
import sys

os.environ['KIVY_HOME'] = sys.path[0]

from menus import *
from filters import FILTER_LIST

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
import kivy.properties as kp
kivy.require('2.0.0')


class AppMenuALayout(AnchorLayout):
    pass


class MainLayout(FloatLayout):
    pass


class MainWindow(App):
    design_graph = kp.ObjectProperty(DesignGraph())
    graph = kp.ObjectProperty()
    main_menu = kp.ObjectProperty()
    menus = kp.ListProperty([])
    main_wnd_view = kp.ObjectProperty()
    loaded_filters = kp.ListProperty()

    def load_known_filters(self):
        for fclass in FILTER_LIST:
            self.loaded_filters.append(fclass)
            print(fclass)

    def get_concrete_menu(self, menu_class):
        for menu in self.menus:
            if issubclass(menu.__class__, menu_class):
                return menu

    def on_graph(self, instance, value):
        """change graph widget in desired place"""
        grid = self.main_wnd_view.ids['place_for_graph']
        try:
            grid.remove_widget(grid.children[0])
        except: pass
        grid.add_widget(self.graph)

    def set_menus(self):
        """set list of menus accessible in program"""
        mainmenu = [w for w in self.main_wnd_view.walk() if issubclass(w.__class__, MainMenu)][0]
        for item in mainmenu.walk():
            try:
                submenu = item.get_submenu()
                if issubclass(submenu.__class__, ContextMenu):
                    submenu.visible = False
                    self.menus.append(submenu)
            except: pass
        self.menus.insert(0, mainmenu)

    def set_graph(self, which_one):
        if which_one == 'visual':
            self.graph = VisualGraph()
        elif which_one == 'design':
            self.graph = self.design_graph
        else:
            self.graph = self.design_graph

    def build(self):
        Config.set('input', 'mouse', 'mouse, disable_multitouch')
        Config.write()
        # utworzenie obiektów opcji w klasie głównej programu
        # mm = Builder.load_file("main_menu.kv")
        self.main_wnd_view = Builder.load_file("main_window.kv")
        self.set_graph('design')
        # self.main_wnd_view.ids['place_for_graph'].add_widget(self.graph)
        self.load_known_filters()
        DesignMenu.load()
        self.set_menus()
        # main_wnd_view.add_widget(mm)
        return self.main_wnd_view


if __name__ == '__main__':
    MainWindow().run()
