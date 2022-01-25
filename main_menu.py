from kivy_garden.contextmenu import AppMenu, ContextMenu,\
    AppMenuTextItem, ContextMenuTextItem

from kivy.properties import ListProperty

from configs import *

class FileMenu(ContextMenu):
    """ klasa odpowiadajaca za menu pliku """
    def __init__(self, main_options, **kwargs):
        super().__init__(**kwargs)
        self.text = 'File'
        self.mo = main_options
        # tworzenie podmenu dla filtra.
        filter_submenu = ContextMenuTextItem(text='Filter')
        fs_submenu = ContextMenu()
        fs_submenu.add_text_item('Open', self.open_filter_cb)
        fs_submenu.add_text_item('Save', self.save_filter_cb)
        filter_submenu.add_widget(fs_submenu) # dodanie do podmenu (kontekst.)
        # tworzenie podmenu dla audio
        audio_submenu = ContextMenuTextItem(text='Audio')
        au_submenu = ContextMenu()
        au_submenu.add_text_item('Open', self.open_audio_cb)
        au_submenu.add_text_item('Save', self.save_audio_cb)
        audio_submenu.add_widget(au_submenu) # dodanie do podmenu (kontekst.)
        # dodawanie utworzonych podmenu-ów do menu pliku.
        self.add_widget(audio_submenu)
        self.add_widget(filter_submenu)

    def open_audio_cb(self):
        print('open_audio_cb release')
        # Dialog z wyborem pliku i załadowaniem scieżki,
        # nie trzeba od poczatku ladowac pliku.
        # mo.audio_path = '/path/to/audio'
        pass

    def save_audio_cb(self):
        print('save_audio_cb release')
        pass

    def open_filter_cb(self):
        print('open_filter_cb release')
        pass

    def save_filter_cb(self):
        print('save_filter_cb release')
        pass



class MainMenu(AppMenu):
    menu_items = ListProperty([])
    def __init__(self, main_options, design_options, visual_options, **kwargs):
        super().__init__(**kwargs)
        self.m_opts = main_options
        self.d_opts = design_options
        self.v_opts = visual_options
        # self.menu_items.append(FileMenu(self.m_opts))
        filemenu = AppMenuTextItem(text='FILE')
        # filemenu.add_widget(FileMenu(self.m_opts))
        cm = ContextMenu()
        cm.add_text_item('cos')
        cm.add_text_item('ktos')
        cm.add_text_item('nikt')
        filemenu.add_widget(cm)
        self.menu_items.append(filemenu)
        self.menu_items.append(AppMenuTextItem(text='EDIT'))

    def on_menu_items(self, inst, values):
        """ metoda wywoływana kiedy zmienią się elementy menu """
        self.clear_widgets()
        for item in values:
            self.add_widget(item)
            self.update_height()


