from kivy.app import App

from . import IFilter
from scipy.interpolate import CubicSpline
from scipy.signal import firls, freqz
import numpy as np
from kivy_garden.graph import MeshLinePlot


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'

    def __init__(self):
        self._coeffs = None
        self._ir = None

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        x, y = zip(*points)
        # XXX Can use interpolation method from profile
        cs = CubicSpline(x, y)
        x = np.arange(min(cs.x), max(cs.x))
        y = list(map(lambda v: np.power(10, v), cs(x)))
        self._coeffs = firls(73, x, y, fs=44100)

    def impulse_response(self):
        if self._ir is not None:
            return self._ir
        freq, response = freqz(self._coeffs)
        points = zip(22000*freq/np.pi, np.log10(response)/10)
        points = filter(lambda x: x[0] >= 18, points)
        self._ir = points
        return self._ir

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass