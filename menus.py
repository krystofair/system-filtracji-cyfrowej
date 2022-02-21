import os.path

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.contextmenu import AppMenu, ContextMenu,\
    AppMenuTextItem, ContextMenuTextItem, ContextMenuDivider

import kivy.properties as kp
from custom_graphs import VisualGraph

def hide_all(self):
    mainmenu = self.parent.parent
    if not issubclass(mainmenu.__class__, MainMenu):
        mainmenu = [x for x in mainmenu.walk_reverse() if issubclass(x.__class__, MainMenu)][0]
        print(mainmenu)
    mainmenu.close_all()
    mainmenu._cancel_hover_timer()


class FileMenu(ContextMenu):
    app_mode = kp.StringProperty('design')
    audio_path = kp.StringProperty('')
    filter_path = kp.StringProperty('')
    audio_fd = kp.ObjectProperty(None)
    filter_fd = kp.ObjectProperty(None)
    chosen_option = kp.StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = {
            'open_audio_cb': self.open_audio_cb,
            'save_audio_cb': self.save_audio_cb,
            'open_filter_cb': self.open_filter_cb,
            'save_filter_cb': self.save_filter_cb,
            'exit_option': self.exit_option
        }

    @staticmethod
    def load():
        menu_item = AppMenuTextItem(text='FILE')
        return menu_item

    def open_audio_cb(self):
        print('open_audio_cb release')
        # Dialog z wyborem pliku i załadowaniem scieżki,
        # nie trzeba od poczatku ladowac pliku.
        # mo.audio_path = '/path/to/audio'

    def save_audio_cb(self):
        print('save_audio_cb release')

    def open_filter_cb(self):
        print('open_filter_cb release')

    def save_filter_cb(self):
        print('save_filter_cb release')

    def exit_option(self):
        exit(0)

    def on_chosen_option(self, instance, value):
        if value == '':
            return
        self.options[self.chosen_option]()
        hide_all(self)
        self.chosen_option = ''


class VisualizationMenu(ContextMenu):
    ready_samples = kp.BooleanProperty(False)
    original_samples = kp.ObjectProperty()
    tovisual_samples = kp.ObjectProperty()
    domain = kp.StringProperty('frequency')
    visual_graph = kp.ObjectProperty()
    play = kp.BooleanProperty(False)
    stop = kp.BooleanProperty(True)

    @staticmethod
    def load():
        from kivy.app import App
        app_instance = App.get_running_app()
        try:
            dynamic_menu_item = app_instance.main_wnd_view.ids['dynamic_menu']
            if dynamic_menu_item.get_submenu() is not None:
                dynamic_menu_item.parent.remove_widget(dynamic_menu_item.get_submenu())
            dynamic_menu_item.text = "VISUAL OPTIONS"
            path = os.path.dirname(os.path.realpath(__file__))
            dm = Builder.load_file(os.path.join(path, 'gui_menus/visual_submenu.kv'))
            dynamic_menu_item.add_widget(dm)
            dm._on_visible(False)
            app_instance.set_graph('visual')
        except Exception as e:
            print("An exception has occured ", e)

    def on_domain(self, instance, value):
        # domain = value if value == 'time' or value == 'frequency' else 'frequency'
        # if self.visual_graph is None:
        #     self.visual_graph = VisualGraph()
        # if domain == 'frequency':
        #     self.visual_graph.xlog = True
        # elif domain == 'time':
        #     self.visual_graph.xlog = False
        hide_all(self)

    def get_sample(self):
        for sample in self.tovisual_samples:
            yield sample

    def on_play(self, inst, value):
        if value:
            self.stop = False
            print('start clock interval, some thread?')
            # start clock interval.
            hide_all(self)

    def on_stop(self, inst, value):
        if value:
            # stop interval
            print('stop interval')
            self.play = False
            hide_all(self)


class DesignMenu(ContextMenu):
    kind_of_filter = kp.StringProperty('fir')
    interpolation = kp.StringProperty('cubic')
    filter_algorithm = kp.ObjectProperty(None)
    start = kp.BooleanProperty(False)

    @staticmethod
    def load():
        from kivy.app import App
        app_instance = App.get_running_app()
        try:
            dynamic_menu_item = app_instance.main_wnd_view.ids['dynamic_menu']
            if dynamic_menu_item.get_submenu() is not None:
                dynamic_menu_item.parent.remove_widget(dynamic_menu_item.get_submenu())
            dynamic_menu_item.text = "DESIGN OPTIONS"
            path = os.path.dirname(os.path.realpath(__file__))
            dm = Builder.load_file(os.path.join(path, 'gui_menus/design_submenu.kv'))
            dynamic_menu_item.add_widget(dm)
            dm._on_visible(False)
            app_instance.set_graph('design')
        except Exception as e: print('exception', e)

    def on_interpolation(self, i, value):
        if value == 'cubic':
            print(value)
        elif value == 'linear':
            print(value)
        else:
            print('nie znana interpolacja')
        hide_all(i)

    def on_kind_of_filter(self, i, v):
        print('on-kind-of-filter')
        hide_all(self)

    def on_filter_algorithm(self, i, v):
        print('on-filter-algorithm')
        hide_all(self)

    def on_start(self, i, v):
        print('on-start')
        hide_all(self)


class ModeMenu(ContextMenu):
    chosen_mode = kp.StringProperty('design')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = {
            'design': self.load_design_option_menu,
            'visualization': self.load_visual_option_menu
        }

    def on_chosen_mode(self, inst, value):
        mainmenu = self.parent.parent
        self.options[value]()
        mainmenu.close_all()
        mainmenu._cancel_hover_timer()

    def load_design_option_menu(self):
        DesignMenu.load()

    def load_visual_option_menu(self):
        VisualizationMenu.load()


class MainMenu(AppMenu):
    pass

