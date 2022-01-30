""" Plik `configs` zawiera klasy, które przechowują konfigurację
dla wybranych trybów. Tryby te zawierają opcje dostepne w menu.
W pierwszej wersji jako wartosci opcji to napisy, lecz po refaktoryzacjach
będzie to zmieniane.
TODO: Ustawić wartości opcji jako stany,
przykład:
    KOF_FIR = 0x01
    KOF_IIR = 0x02
    DM_CUBIC = 0x01
"""

import kivy.properties as kp



class MainOptions:
    """ Głowne opcje programu """
    # app_mode    = kp.StringProperty('design')
    # audio_path  = kp.StringProperty('')
    # filter_path = kp.StringProperty('')
    # audio_fd    = kp.ObjectProperty(None)
    # filter_fd   = kp.ObjectProperty(None)
    def __init__(self):
        # opcja wybranego trybu
        self.app_mode = 'design' # tryb dzialania aplikacji
        self.audio_path = '' # sciezka pliku audio
        self.filter_path = '' # sciezka pliku filtra
        self.filter_fd = None # plik filtra
        self.audio_fd = None # plik audio


class DesignOptions:
    """ Opcje dla trybu projektowania """
    def __init__(self):
        # kind_of_filter jest rodzajem filtru NOI lub SOI
        self.kind_of_filter = 'fir'
        # drawing mode stands for how line will be behaving
        self.draw_mode = 'cubic'
        # ...
        # self.


class VisualizationOptions:
    """ Opcje trybu wizualizacji """
    def __init__(self):
        # probki przetworzone
        self.processed_samples = None
        # probki oryginalne
        self.original_samples = None
        # jeśli time to próbki są wyświetlene tak jak w audacity
        # inaczej stale się zmieniają na okreslonych pozycjach
        self.domain = 'time' # albo 'freq'
