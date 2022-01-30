from kivy_garden.contextmenu import AppMenu, ContextMenu, AppMenuTextItem, ContextMenuTextItem, ContextMenuDivider

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

class FileMenu(ContextMenu):
    """ klasa odpowiadajaca za menu pliku """

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

class ModeMenu(ContextMenu):
    chosen_mode = StringProperty()
    options = ObjectProperty()
    main_menu = ObjectProperty()

    def on_chosen_mode(self, inst, value):
        if value == 'design':
            Builder.load_file('design_submenu.kv')
        elif value == 'visualization':
            Builder.load_file('visual_submenu.kv')
        self.main_menu.add_widget()



class MainMenu(AppMenu):
    m_opts = ObjectProperty(MainOptions())
    d_opts = ObjectProperty(DesignOptions())
    v_opts = ObjectProperty(VisualOptions())
    pass


