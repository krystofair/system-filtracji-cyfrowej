import os.path
from functools import partial

from kivy.app import App
from kivy.lang import Builder
from kivy_garden.contextmenu import AppMenu, ContextMenu, \
    AppMenuTextItem, ContextMenuTextItem, ContextMenuDivider

import kivy.properties as kp
#todo zaimportuj tutaj modal window kivy
from custom_graphs import VisualGraph, DesignGraph
from scipy.interpolate import CubicSpline, interp1d


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
            'load_audio_cb': self.load_audio_cb,
            'save_audio_cb': self.save_audio_cb,
            'load_filter_cb': self.load_filter_cb,
            'save_filter_cb': self.save_filter_cb,
            'exit_option': self.exit_option
        }

    def load_audio_cb(self):
        print('load_audio_cb release')
        # Dialog z wyborem pliku i załadowaniem scieżki,
        # nie trzeba od poczatku ladowac pliku.
        # mo.audio_path = '/path/to/audio'

    def save_audio_cb(self):
        print('save_audio_cb release')

    def load_filter_cb(self):

        print('load_filter_cb release')

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
            return dm
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
    filter = kp.StringProperty()  # interfejs do wyboru filtru
    interpolation = kp.StringProperty('cubic')
    start = kp.BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filter = None

    @staticmethod
    def reset_design_graph():
        app = App.get_running_app()
        app.design_graph = DesignGraph()
        app.set_graph('design')

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
            dm.load_filter_list()
            dynamic_menu_item.add_widget(dm)
            dm._on_visible(False)
            app_instance.set_graph('design')
            return dm
        except Exception as e:
            print('exception', e)

    def load_filter_list(self):
        filters_names_list = self.ids['filters_names_list']
        app_instance = App.get_running_app()
        filters_classes_list = app_instance.loaded_filters

        def release_callback(this):
            self.filter = this.text

        for fc in filters_classes_list:
            t = fc.filter_id+'#'+fc.filter_kind
            cmti = ContextMenuTextItem(text=t)
            cmti.on_release = partial(release_callback, cmti)
            filters_names_list.add_widget(cmti)

    def on_interpolation(self, i, value):
        app = App.get_running_app()
        if value == 'cubic':
            app.design_graph.custom_plot.interp_func = CubicSpline
        elif value == 'linear':
            app.design_graph.custom_plot.interp_func = interp1d
        else:
            raise Exception("Interpolation not known.")
        hide_all(i)

    def on_filter(self, i, v):
        app_instance = App.get_running_app()
        filter_list = app_instance.loaded_filters
        id = v[:v.index('#')]
        for filter_item in filter_list:
            if id == filter_item.filter_id:
                self._filter = filter_item()  # creating instance of filter class
        hide_all(self)

    def on_start(self, i, v):
        app = App.get_running_app()
        app.design_graph.get_profile()
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
        App.get_running_app().set_menus()

    def load_visual_option_menu(self):
        VisualizationMenu.load()
        App.get_running_app().set_menus()


class MainMenu(AppMenu):
    pass