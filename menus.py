#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import os.path
from functools import partial

import custom_plots
import kivy.properties as kp
# todo zaimportuj tutaj popup kivy
from custom_graphs import DesignGraph
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy_garden.contextmenu import AppMenu, ContextMenu, ContextMenuTextItem, AppMenuTextItem
from interpolation_funcs import INTERPOLATION_FUNCTIONS


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
        # TODO: Dialog z wyborem pliku i załadowaniem scieżki,
        # nie trzeba od poczatku ladowac pliku.
        # mo.audio_path = '/path/to/audio'

    def save_audio_cb(self):
        print('save_audio_cb release')

    def load_filter_cb(self):
        print('load_filter_cb release')
        # print(self.)

    def save_filter_cb(self):
        print('save_filter_cb release')

    def exit_option(self):
        exit(0)

    def on_chosen_option(self, instance, value):
        if value == '':
            return
        self.options[self.chosen_option]()
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
        pass

    def get_sample(self):
        for sample in self.tovisual_samples:
            yield sample

    def on_play(self, inst, value):
        if value:
            self.stop = False
            print('start clock interval, some thread?')
            # start clock interval.

    def on_stop(self, inst, value):
        if value:
            # stop interval
            print('stop interval')
            self.play = False


class DesignMenu(ContextMenu):
    filter = kp.StringProperty()
    interpolation = kp.StringProperty('cubic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filter = None

    def reset_design_graph(self):
        app = App.get_running_app()
        app.design_graph = DesignGraph()
        self.on_interpolation(self, self.interpolation)
        app.set_graph('design')

    @staticmethod
    def reset_filter_plot():
        app = App.get_running_app()
        for plot in app.design_graph.plots[:]:
            if isinstance(plot, custom_plots.FilterPlot):
                app.design_graph.remove_plot(plot)

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
        """ Loading list of accessible filters """
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

    @staticmethod
    def on_interpolation(i, value):
        app = App.get_running_app()
        if value == 'cubic':
            app.design_graph.design_plot.interp_func = INTERPOLATION_FUNCTIONS['cubic']
        elif value == 'linear':
            app.design_graph.design_plot.interp_func = INTERPOLATION_FUNCTIONS['linear']
        else:
            raise Exception("Interpolation not known.")

    def on_filter(self, i, v):
        """Method is called when someone choose filter from the list.
        Here, the filter instance is created and stored in internal state of
        class `DesignMenu` instance."""
        if self.filter == '':
            return
        app_instance = App.get_running_app()
        filter_list = app_instance.loaded_filters
        id = v[:v.index('#')]
        for filter_item in filter_list:
            if id == filter_item.filter_id:
                self._filter = filter_item()
        # checking appropriate implementation of filter 'menu' method.
        filter_context_menu = self._filter.menu()
        if not filter_context_menu or not isinstance(filter_context_menu, FilterMenu):
            # If filter doesn't have own menu, here is creating simple FilterMenu(ContextMenu)
            filter_context_menu = FilterMenu()
        # deleting old "filter options" menu
        for lam in reversed(app_instance.menus):
            if isinstance(lam, FilterMenu):
                app_instance.menus[0].remove_widget(lam.orig_parent or lam.parent)
                break
        # creating new "filter options" menu
        menu_item = AppMenuTextItem(text='FILTER OPTIONS')
        menu_item.add_widget(filter_context_menu)
        if self._filter.description() is not None:
            popup_desc = ContextMenuTextItem(text='Show description')
            popup = Popup(title="Filter description (escape to quit)",
                          content=Label(text=self._filter.description()))
            popup_desc.bind(on_release=lambda x: popup.open())
            filter_context_menu.add_widget(popup_desc)
        filter_context_menu.add_widget(
            ContextMenuTextItem(text='Create', color=[1,0,0,1],
                                on_release=partial(self.create_filter_callback, self)))
        app_instance.menus[0].add_widget(menu_item)
        filter_context_menu._on_visible(False)
        filter_context_menu.show()
        filter_context_menu.hide()
        app_instance.set_menus()

    def create_filter_callback(self, inst, value):
        app = App.get_running_app()
        if self._filter is not None:
            self._filter.generate_filter(app.design_graph.design_plot)
            plot = custom_plots.FilterPlot(points=self._filter.frequency_response(),
                                           color=[0, 0, 1, 1])
            app.design_graph.add_plot(plot)

    @staticmethod
    def save_profile():
        app = App.get_running_app()
        # TODO: dialog for choice a path.
        path = "profile.chr"
        app.design_graph.design_plot.save_profile(path)

    @staticmethod
    def load_profile():
        app = App.get_running_app()
        # TODO: dialog for choice a path.
        path = "profile.chr"
        app.design_graph.design_plot.load_profile(path)


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
    def collide_point(self, x, y):
        for item in self.walk():
            try:
                submenu = item.get_submenu()
                if submenu.visible and submenu.self_or_submenu_collide_with_point(x, y):
                    return True
            except: pass
        return super().collide_point(x, y)


class FilterMenu(ContextMenu):
    """Class created for filters options and in order to differentiate objects instances."""
    pass
