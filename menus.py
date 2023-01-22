#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import os.path
import random
import subprocess
from functools import partial

import dialogs
import soundfile
import store
import threading

import custom_plots
import kivy.properties as kp
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy_garden.contextmenu import AppMenu, ContextMenu, ContextMenuTextItem, AppMenuTextItem

from custom_graphs import DesignGraph
from interpolation_funcs import INTERPOLATION_FUNCTIONS
import audio


def do_block_from_str(string, size):
    result = []
    s = string
    while len(s) > size:
        part1, part2 = s[:size], s[size:]
        result.append(part1)
        s = part2
    if len(s) != 0:
        result.append(s)
    return '\n'.join(result)


class FileMenu(ContextMenu):
    app_mode = kp.StringProperty('design')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_audio_from_file(self):
        # this dialog after choose file update value in store
        dialogs.audio_file_chooser_dialog('.')

    def processing_view_window(self):
        Logger.info('processing_view_window callback release')
        content = store.get('processing-progress')
        popup = Popup(title="State of processing",
                      content=Label(text=content if content else "unknown"))
        popup.size_hint = (0.8, 0.8)
        popup.open()

    def save_audio(self):
        if any([True for file in os.listdir('.') if file == audio.TMP_FILE]):
            dialogs.SaveDialog(self.save_as)
        else:
            popup = Popup(title="Error",
                          content=Label(text="There was not processing yet."),
                          size_hint=(0.8, 0.8))
            popup.open()

    def save_as(self, path):
        cp = None
        try:
            cp = subprocess.run(['copy', audio.TMP_FILE, path], capture_output=True)
        except FileNotFoundError:
            cp = subprocess.run(['cp', audio.TMP_FILE, path])

        if cp and cp.returncode == 0:
            popup = Popup(title="Success",
                          content=Label(text="File was saved."),
                          size_hint=(0.8, 0.8))
            popup.open()

    # def load_filter_from_file(self):
    #     Logger.info('load_filter_cb release')
    #
    # def save_filter_to_file(self):
    #     Logger.info('save_filter_cb release')

    def exit(self):
        try:
            os.remove(audio.TMP_FILE)
        except Exception as e:
            Logger.info(f"Tmp file cannot be removed {e}")
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

    def random_color(self):
        return [random.random(), random.random(), random.random(), 1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filter = None
        self._audio_processing_thread = None
        self.color_pointer = 0

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
                store.add_or_update('loaded-filter', self._filter)
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
        menu_item = AppMenuTextItem(text=f'{self._filter.filter_id} OPTIONS')
        menu_item.add_widget(filter_context_menu)
        if self._filter.description() is not None:
            popup_desc = ContextMenuTextItem(text='Show description')
            popup = Popup(title="Filter description (escape to quit)",
                          content=Label(text=self._filter.description()),
                          size_hint=(0.8, 0.8))
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

    def show_popup_with_choosing_audio_file(self):
        popup = Popup(title="Audio file to process does not chosen.",
                      content=Label(text="You should click on FILE menu then use option\n"
                                         "'Open audio file' and do double click when you\n"
                                         "find a file you want to process with filter."))
        popup.size_hint = (0.8, 0.8)
        popup.open()

    def create_filter_callback(self, inst, value):
        app = App.get_running_app()
        sample_rate = audio.get_sample_rate_from_file()
        if sample_rate is None:
            self.show_popup_with_choosing_audio_file()
            return
        if self._filter is not None:
            self._filter.generate_filter(app.design_graph.design_plot, sample_rate)
            plot = custom_plots.FilterPlot(points=self._filter.frequency_response(),
                                           color=self.random_color())
            app.design_graph.add_plot(plot)

    def apply_filter_callback(self, inst, value):
        if self._audio_processing_thread is not None and self._audio_processing_thread.is_alive():
            popup = Popup(title="Processing is already started.",
                          content=Label(text="Wait for processing to finish."))
            popup.size_hint = (0.8, 0.8)
            popup.open()
            return
        app = App.get_running_app()
        fs = audio.get_sample_rate_from_file()
        if fs is None:
            self.show_popup_with_choosing_audio_file()
            return
        file_path = store.get('audio-file-path')[0]
        try:
            self._filter.generate_filter(app.design_graph.design_plot, fs)
        except Exception as e:
            popup = Popup(title="Generating filter failed.",
                          content=Label(text=do_block_from_str(str(e), 100)))
            popup.size_hint = (0.8, 0.8)
            popup.open()

        def thread_worker():
            store.add('processing-progress', 'started')
            audio.processing_samples(file_path, self._filter)
            # p = Popup(title="Processing file ended.",
            #           content=Label(text="Processing samples has been ended."))
            # p.open()
            if not store.get('processing-exception'):
                store.add_or_update('processing-progress', 'finished')
            pb = store.get('progress-bar')
            ppc = store.get('popup-processing-content')
            if pb and ppc:
                ppc.remove_widget(pb)
                store.delete('progress-bar')
                store.delete('popup-processing-content')

        progress_bar = ProgressBar(max=100)
        store.add('progress-bar', progress_bar)
        grid_layout = GridLayout(rows=2, orientation='tb-lr')
        grid_layout.add_widget(Label(text="File is processing.\n"
                                          "You can check status in file menu if you close this popup."))
        grid_layout.add_widget(progress_bar)
        store.add('popup-processing-content', grid_layout)
        self._audio_processing_thread = threading.Thread(target=thread_worker)
        self._audio_processing_thread.start()
        popup = Popup(title="Processing file.", content=grid_layout, size_hint=(0.8, 0.8))
        popup.open()

    @staticmethod
    def save_profile():
        app = App.get_running_app()
        dialogs.SaveDialog(app.design_graph.design_plot.save_profile)

    @staticmethod
    def load_profile():
        app = App.get_running_app()

        def _aaaa():
            a = App.get_running_app()
            a.get_concrete_menu(DesignMenu).interpolation = store.get('interpolation-function')

        dialogs.profile_chooser_dialog('.', app.design_graph.design_plot.load_profile, _aaaa)


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
