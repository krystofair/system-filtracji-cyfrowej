from kivy_garden.contextmenu import AppMenu, ContextMenu,\
    AppMenuTextItem, ContextMenuTextItem, ContextMenuDivider

from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder
from configs import *


class FileMenu(MainOptions, ContextMenu):
    KV_MENU_STR = """

    """
    options = kp.ObjectProperty(None)
    @staticmethod
    def load():
        menu_item = AppMenuTextItem(text='FILE')
        this = Builder.load_string(FileMenu.KV_MENU_STR)
        menu_item.submenu = this
        return menu_item

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


class VisualizationMenu(VisualizationOptions, ContextMenu):
    @staticmethod
    def load():
        menu_item = AppMenuTextItem(text='VISUAL OPTIONS')
        this = VisualizationMenu()
        this.add_text_item('nie wiem', on_release=this.opcja1)
        this.add_text_item('opcja2', on_release=this.opcja2)
        menu_item.submenu = this
        return menu_item


class DesignMenu(DesignOptions, ContextMenu):
    options = kp.ObjectProperty()

    @staticmethod
    def load():
        menu_item = AppMenuTextItem(text='DESIGN OPTIONS')
        this = DesignMenu()
        this.add_text_item('opcja1', on_release=this.opcja1)
        this.add_text_item('opcja2', on_release=this.opcja2)
        menu_item.submenu = this
        return menu_item


class ModeMenu(ContextMenu):
    choose_mode = StringProperty('design')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_choose_mode(self, inst, value):

        self.hide()


class MainMenu(AppMenu): pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     filemenu = FileMenu.load()
    #     self.add_widget(filemenu)
    #     additional_menu = DesignMenu.load()
    #     self.add_widget(additional_menu)
    #     for child in self.children[:]:
    #         if isinstance(child, ModeMenu):
    #             child.dynamic_menu = additional_menu
