""" Plik `configs` zawiera klasy, które przechowują konfigurację
dla wybranych trybów. Tryby te zawierają opcje dostepne w menu.
W pierwszej wersji jako wartosci opcji to napisy, lecz po refaktoryzacjach
będzie to zmieniane. """

import kivy.properties as kp
from custom_graphs import VisualGraph



class MainOptions:
    app_mode = kp.StringProperty('design')
    audio_path = kp.StringProperty('')
    filter_path = kp.StringProperty('')
    audio_fd = kp.ObjectProperty(None)
    filter_fd = kp.ObjectProperty(None)


class DesignOptions:
    kind_of_filter = kp.StringProperty('fir')
    interpolation = kp.StringProperty('cubic')
    filter_algorithm = kp.ObjectProperty(None)
    start = kp.BooleanProperty(False)


class VisualizationOptions:
    ready_samples = kp.BooleanProperty(False)
    original_samples = kp.ObjectProperty()
    tovisual_samples = kp.ObjectProperty()
    domain = kp.StringProperty('frequency')
    visual_graph = kp.ObjectProperty()
    play = kp.BooleanProperty(False)
    stop = kp.BooleanProperty(True)

    def on_domain(self, instance, value):
        domain = value if value == 'time' or value == 'frequency' else 'frequency'
        if self.visual_graph is None: self.visual_graph = VisualGraph()
        if domain == 'frequency':
            self.visual_graph.xlog = True
        else:
            self.visual_graph.xlog = False

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
