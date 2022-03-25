from . import IFilter
from scipy.interpolate import CubicSpline
from scipy.signal import firls, freqz
import numpy as np


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'

    def __init__(self):
        self._coeffs = None

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        if len(points) < 2:
            return
        freqs, amplitudes = zip(*points)
        # XXX Can use interpolation method from profile
        try:
            interpolation = profile.interp_func(freqs, amplitudes)
        except:
            interpolation = CubicSpline(freqs, amplitudes)
        bands = list(range(freqs[0], freqs[len(freqs)-1]))
        bands.append(bands[len(bands)-1]) if not len(bands) % 2 == 0 else None
        # TODO: change the way of grouping band to pythonist way.
        b = []
        for i in range(int(len(bands)/2)):
            b.append([bands[i], bands[i+1]])
        desired = np.power(10, interpolation(bands)/20)
        self._coeffs = firls(99, b, desired, fs=44100)

    def frequency_response(self):
        if self._coeffs is None:
            return []
        freq, response = freqz(self._coeffs, fs=44100)
        ir_points = zip(freq, np.abs(response))
        return ir_points

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass