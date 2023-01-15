#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

import os

from menus import *
from filters import FILTER_LIST
from cursor_bubble import CursorPosBubble
import store

import kivy
from kivy.logger import Logger
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
    menus = kp.ListProperty([])
    main_wnd_view = kp.ObjectProperty()
    loaded_filters = kp.ListProperty()
    cursor_bubble = kp.ObjectProperty(CursorPosBubble())

    def load_known_filters(self):
        for fclass in FILTER_LIST:
            self.loaded_filters.append(fclass)

    def get_concrete_menu(self, menu_class):
        for menu in self.menus:
            if issubclass(menu.__class__, menu_class):
                return menu

    def on_graph(self, instance, value):
        """change graph widget in desired place"""
        grid = self.main_wnd_view.ids['place_for_graph']
        try:
            grid.remove_widget(grid.children[0])
        except Exception as e:
            Logger.exception(e)
        grid.add_widget(self.graph)
        self.cursor_bubble.graph = self.graph

    def set_menus(self):
        """set list of menus accessible in program"""
        self.menus.clear()
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
        store.update('current-graph', which_one)
        if which_one == 'visual':
            self.graph = VisualGraph()
        elif which_one == 'design':
            self.graph = self.design_graph
        else:
            raise ValueError(f"The graph {which_one} does not exist.")

    def configure_kivy(self):
        _path = os.path.dirname(os.path.realpath(__file__))
        os.environ['KIVY_HOME'] = _path
        Config.read(os.path.join(_path, 'config.ini'))
        Config.set('kivy', 'exit_on_escape', 0)
        Config.set('kivy', 'log_maxfiles', 1)
        Config.set('kivy', 'log_dir', os.path.join(_path, "logs"))
        Config.set('input', 'mouse', 'mouse, disable_multitouch')
        Config.set('graphics', 'height', 764)
        Config.set('graphics', 'width', 1024)
        Config.set('graphics', 'minimum_height', 600)
        Config.set('graphics', 'minimum_width', 800)
        Config.set('graphics', 'maxfps', 30)
        Config.write()

    def build(self):
        import store  # important because this create store for first time.
        self.configure_kivy()
        self.title = "System Filtracji Cyfrowej"
        # utworzenie obiektów opcji w klasie głównej programu
        self.main_wnd_view = Builder.load_file("main_window.kv")
        self.set_graph('design')
        store.add('current-graph', 'design')
        self.load_known_filters()
        DesignMenu.load()
        self.set_menus()
        self.main_wnd_view.add_widget(self.cursor_bubble)
        return self.main_wnd_view


if __name__ == '__main__':
    MainWindow().run()
