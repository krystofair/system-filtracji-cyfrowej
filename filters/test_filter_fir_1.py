from . import IFilter
from scipy.interpolate import CubicSpline
from scipy.signal import firls
import numpy as np


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'

    def __init__(self):
        self._coeffs = None

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        x, y = zip(*points)
        cs = CubicSpline(x, y)
        x = np.arange(min(cs.x), max(cs.x))
        self._coeffs = firls(99, x, cs, fs=44100)

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass