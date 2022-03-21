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

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        x, y = zip(*points)
        # XXX Can use interpolation method from profile
        cs = CubicSpline(x, y)
        x = np.arange(min(cs.x), max(cs.x))
        y = list(map(lambda v: np.power(10, v), cs(x)))
        self._coeffs = firls(999, x, y, fs=44100)

    def impulse_response(self):
        if self._coeffs is None:
            return []
        freq, response = freqz(self._coeffs)
        ir_points = zip(freq, np.log10(response))
        # ir_points = filter(lambda x: x[0] >= 18, ir_points)
        return ir_points

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass