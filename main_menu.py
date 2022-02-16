from kivy_garden.contextmenu import AppMenu, ContextMenu, AppMenuTextItem, ContextMenuTextItem, ContextMenuDivider

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.lang import Builder

from configs import *

class FileMenu(ContextMenu):

    def open_audio_cb(self):
        print('open_audio_cb release')
        # Dialog z wyborem pliku i załadowaniem scieżki,
        # nie trzeba od poczatku ladowac pliku.
        # mo.audio_path = '/path/to/audio'
        self.hide()

    def save_audio_cb(self):
        print('save_audio_cb release')
        self.hide()

    def open_filter_cb(self):
        print('open_filter_cb release')
        self.hide()

    def save_filter_cb(self):
        print('save_filter_cb release')
        self.hide()

    def exit_option(self):
        exit(0)


class ModeMenu(ContextMenu):
    choose_mode = StringProperty()
    options = ObjectProperty()
    # main_menu = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_choose_mode(self, inst, value):
        try:
            self.parent.main_menu.remove_widget(self.dynamic_menu)
        except: pass
        if value == 'design':
            self.dynamic_menu = Builder.load_file('design_submenu.kv')
        elif value == 'visualization':
            self.dynamic_menu = Builder.load_file('visual_submenu.kv')
        try:
            self.parent.main_menu.add_widget(self.dynamic_menu)
        except Exception as e:
            print(e)
        self.hide()



class MainMenu(AppMenu):
    m_opts = ObjectProperty(MainOptions())
    d_opts = ObjectProperty(DesignOptions())
    v_opts = ObjectProperty(VisualizationOptions())

    def on_touch_down(self, touch):
        for child in self.children:
            child.on_touch_down(touch)
        return False
    pass

class VisualizationMenu(ContextMenu):

    def cos(self):
        pass
    pass

class DesignMenu(ContextMenu):
    """ callbacks for options """
    pass

