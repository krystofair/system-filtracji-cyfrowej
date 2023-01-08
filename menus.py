#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import os.path
from functools import partial

import dialogs
import store
from numpy import ndarray
import threading

import custom_plots
import kivy.properties as kp
import soundfile
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy_garden.contextmenu import AppMenu, ContextMenu, ContextMenuTextItem, AppMenuTextItem

from custom_graphs import DesignGraph
from interpolation_funcs import INTERPOLATION_FUNCTIONS
import audio


class FileMenu(ContextMenu):
    app_mode = kp.StringProperty('design')

    # filter_path = kp.StringProperty('')
    # audio_fd = kp.ObjectProperty(None)
    # filter_fd = kp.ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_audio_from_file(self):
        # this dialog after choose file update value in store
        dialogs.file_chooser_dialog('.')

    def save_audio_to_file(self):
        Logger.info('save_audio callback release')
        content = store.get('processing-progress')
        popup = Popup(title="Filter description (escape to quit)",
                      content=Label(text=content if content else "unknown"))
        popup.open()
    #
    # def load_filter_from_file(self):
    #     Logger.info('load_filter_cb release')
    #
    # def save_filter_to_file(self):
    #     Logger.info('save_filter_cb release')

    def exit(self):
        exit(0)


class VisualizationMenu(ContextMenu):
    ready_samples = kp.BooleanProperty(False)
    original_samples = kp.ObjectProperty()
    processed_samples = kp.ObjectProperty()
    domain = kp.StringProperty('frequency')
    processing_function = kp.ObjectProperty()  # that is conversion function appropriate for domain.
    visual_graph = kp.ObjectProperty()
    play = kp.BooleanProperty(False)
    stop = kp.BooleanProperty(True)

    @staticmethod
    def load():
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
            Logger.exception(e)

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
            Logger.info('start clock interval, some thread?')
            # start clock interval.

    def on_stop(self, inst, value):
        if value:
            # stop interval
            Logger.info('stop interval')
            self.play = False


class DesignMenu(ContextMenu):
    filter = kp.StringProperty()
    interpolation = kp.StringProperty('cubic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filter = None
        self._audio_processing_thread = None

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
            Logger.exception(e)

    def load_filter_list(self):
        """ Loading list of accessible filters """
        filters_names_list = self.ids['filters_names_list']
        app_instance = App.get_running_app()
        filters_classes_list = app_instance.loaded_filters

        def release_callback(this):
            self.filter = this.text

        for fc in filters_classes_list:
            t = fc.filter_id + '#' + fc.filter_kind
            cmti = ContextMenuTextItem(text=t)
            cmti.on_release = partial(release_callback, cmti)
            filters_names_list.add_widget(cmti)

    @staticmethod
    def on_interpolation(i, value):
        app = App.get_running_app()
        try:
            app.design_graph.design_plot.interp_func = INTERPOLATION_FUNCTIONS[value]
        except KeyError as e:
            Logger.error("Interpolation not known.")

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
            ContextMenuTextItem(text='Create',
                                on_release=partial(self.create_filter_callback, self)))
        filter_context_menu.add_widget(
            ContextMenuTextItem(text='Apply', on_release=partial(self.apply_filter_callback, self))
        )
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

    def apply_filter_callback(self, inst, value):
        if self._audio_processing_thread is not None and self._audio_processing_thread.is_alive():
            popup = Popup(title="Processing is already started.",
                          content=Label(text="Wait for processing to finish."))
            popup.open()
            return
        app = App.get_running_app()
        read_file_path = store.get('audio-file-path')
        if read_file_path is None:
            popup = Popup(title="Audio file to process does not chosen.",
                          content=Label(text="You should click on FILE menu then use option\n"
                                             "'Open audio file' and do double click when you\n"
                                             "find a file you want to process with filter."))
            popup.open()
            return
        file_path = read_file_path[0]
        sample_rate = soundfile.info(file_path).samplerate
        channels = soundfile.info(file_path).channels
        self._filter.generate_filter(app.design_graph.design_plot)

        def thread_worker():
            store.add_or_update('processing-progress', 'started')
            data_generator = audio.generator_audio_data(file_path)
            saving_consumer = audio.create_save_consumer('processed.wav', sample_rate, channels)
            audio.processing_samples(data_generator, saving_consumer, self._filter)
            # p = Popup(title="Processing file ended.",
            #           content=Label(text="Processing samples has been ended."))
            # p.open()
            store.add_or_update('processing-progress', 'finished')

        self._audio_processing_thread = threading.Thread(target=thread_worker)
        self._audio_processing_thread.start()
        popup = Popup(title="Processing file.",
                      content=Label(text="File is processing.\n"
                                         "You can check status in file menu."))
        popup.open()

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
        app.get_concrete_menu(DesignMenu).interpolation = store.get('interpolation-function')


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
            except:
                pass
        return super().collide_point(x, y)


class FilterMenu(ContextMenu):
    """Class created for filters options and in order to differentiate objects instances."""
    pass
