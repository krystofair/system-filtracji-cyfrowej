#  Copyright (c) 2023.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
"""
Utils for dialog displaying to user.
"""

from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import store


def file_chooser_dialog(start_path):
    popup = Popup()

    def exit_action(sel, touch):
        store.add("audio-file-path", sel)
        popup.dismiss()
    chooser = FileChooserListView()
    chooser.path = start_path
    chooser.filters = ["*.wav", "*.flac", '*.mp3']
    chooser.on_submit = exit_action
    popup.add_widget(chooser)
    popup.open()



