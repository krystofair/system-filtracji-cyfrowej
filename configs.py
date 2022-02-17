""" Plik `configs` zawiera klasy, które przechowują konfigurację
dla wybranych trybów. Tryby te zawierają opcje dostepne w menu.
W pierwszej wersji jako wartosci opcji to napisy, lecz po refaktoryzacjach
będzie to zmieniane. """

import kivy.properties as kp



class MainOptions:
    """ Głowne opcje programu """
    app_mode    = kp.StringProperty('design')
    audio_path  = kp.StringProperty('')
    filter_path = kp.StringProperty('')
    audio_fd    = kp.ObjectProperty(None)
    filter_fd   = kp.ObjectProperty(None)

    def __init__(self):
        pass


class DesignOptions:
    kind_of_filter = kp.StringProperty('fir')
    draw_mode = kp.StringProperty('cubic')
    pass


class VisualizationOptions:
    processed_samples = kp.BooleanProperty(False)
    original_samples = kp.ListProperty([])
    domain = kp.StringProperty('time')

    def __init__(self):
        pass
