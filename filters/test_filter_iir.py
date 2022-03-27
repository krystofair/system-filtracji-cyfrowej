from .filter_interface import IFilter
import numpy as np

class TestFilterIIR(IFilter):

    filter_id = "TestowyFilterekIIR"
    filter_kind = "iir"

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        if len(points) < 2:
            return
        freqs, amps_dB = zip(*points)
        # XXX Can use interpolation method from profile
        try:
            interpolation = profile.interp_func(freqs, amps_dB)
        except Exception as e:
            print(e)
            return
        bands = list(range(freqs[0], freqs[len(freqs) - 1]))
        bands.append(bands[len(bands) - 1]) if not len(bands) % 2 == 0 else None
        desired = np.power(10, interpolation(bands) / 20)
        try:
            # oblicz współczynniki
            print('alfa i omega')
        except Exception as e:
            # todo pop up for communicate user
            print(e)
            self._coeffs = None

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass

    def frequency_response(self):
        pass

    def phase_response(self):
        pass

    def description(self):
        pass

    def menu(self):
        pass