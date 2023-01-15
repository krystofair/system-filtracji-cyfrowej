#  Copyright (c) 2023.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.


from filters.filter import IFilter
from scipy.signal import butter, lfilter


class HighpassButterWorthFilter(IFilter):
    filter_id = "HighpassButterWorthFilter"
    filter_kind = "iir"

    def __init__(self):
        self.order = 3
        self.b = []
        self.a = [1]
        self.fs = 44100

    def generate_filter(self, profile):
        self.profileXD = profile
        # if len(self.profileXD.get_points_as_list()) == 2:
        #     bands = [x[0] for x in profile.get_points_as_list()]
        if len(self.profileXD.get_points_as_list()) == 1:
            boundary_freq = self.profileXD.get_points_as_list()[0]
            self.b, self.a = butter(3, boundary_freq, btype='bandpass', output='ba', fs=self.fs)

    @classmethod
    def load_filter(cls, bin_file_or_path):
        pass

    def save_filter(self, path):
        pass

    def frequency_response(self):
        return [(x, y + 1) for x, y in self.profileXD.get_points_as_list()]
        pass

    def phase_response(self):
        super().phase_response()

    def description(self):
        return """
        Aby wygenerować ten filtr i móc go użyć, należy usunąć wszystkie punkty z charakterystyki,
        a następnie zaznaczyć tylko jeden punkt na częstotliwości granicznej od której chcemy,
        aby filtr zaczął przepuszczać. Jeśli warunek jednego punktu nie będzie spełniony,
        nie będzie możliwości zaplikowania filtru, ponieważ nie zostaną wygerowane współczynniki."""

    def menu(self):
        return super().menu()

    def process(self, samples, *args, **kwargs):
        channels = len(samples[0])
        return lfilter(self.b, self.a, samples, axis=0)
