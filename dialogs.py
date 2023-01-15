#  Copyright (c) 2023.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
"""
Utils for dialog displaying to user.
"""
import functools

import store
from kivy.lang import builder
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


def audio_file_chooser_dialog(start_path):
    popup = Popup()
    popup.size_hint = (0.9, 0.9)

    def exit_action(sel, touch):
        store.add_or_update("audio-file-path", sel)
        popup.dismiss()
    chooser = FileChooserListView()
    chooser.path = start_path
    chooser.filters = ["*.wav"]
    chooser.on_submit = exit_action
    popup.add_widget(chooser)
    popup.open()


def profile_chooser_dialog(start_path, action, *functions):
    popup = Popup()
    popup.size_hint = (0.9, 0.9)

    def exit_action(a, f, sel, touch):
        a(sel[0])
        for function in f:
            function()
        popup.dismiss()
    chooser = FileChooserListView()
    chooser.path = start_path
    chooser.filters = ["*.chr"]
    chooser.on_submit = functools.partial(exit_action, action, functions)
    popup.add_widget(chooser)
    popup.open()


class SaveDialog:

    def __init__(self, save_action, **kwargs):
        super().__init__(**kwargs)
        self.save_callback = save_action
        self.popup = Popup()
        self.popup.size_hint = (0.9, 0.9)
        self.layout = builder.Builder.load_file("gui/save_dialog.kv")
        self.popup.add_widget(self.layout)
        self.__bind_enter_behaviour()
        self.__bind_save_behaviour()
        self.popup.open()

    def save(self, text_to_validate=None):
        self.save_callback(self.__get_text_from_input())
        self.__close()

    def __close(self):
        builder.Builder.unload_file('gui/save_dialog.kv')
        self.layout = None
        self.popup.dismiss()

    def __bind_enter_behaviour(self):
        self.__get_text_input().bind(on_text_validate=self.save)

    def __get_text_input(self) -> TextInput:
        return [x for x in self.layout.walk() if isinstance(x, TextInput)
                or issubclass(x.__class__, TextInput)][0]

    def __get_text_from_input(self):
        text_input_widget: TextInput = self.__get_text_input()
        return text_input_widget.text

    def __bind_save_behaviour(self):
        for widget in self.layout.walk():
            if isinstance(widget, Button):
                widget.on_release = self.save
