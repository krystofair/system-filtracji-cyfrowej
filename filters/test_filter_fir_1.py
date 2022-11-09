#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from .filter_interface import IFilter, FilterMenu
from scipy.interpolate import CubicSpline
from scipy.signal import firls, freqz
from scipy.signal import lfilter
import numpy as np
from kivy.logger import Logger


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'
    options_menu = None

    def __init__(self):
        self._coeffs = None

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        if len(points) < 2:
            return
        freqs, amps_dB = zip(*points)
        # XXX Can use interpolation method from profile
        try:
            interpolation = profile.interp_func(freqs, amps_dB)
        except:
            interpolation = CubicSpline(freqs, amps_dB)
        bands = list(range(freqs[0], freqs[len(freqs) - 1]))
        bands.append(bands[len(bands) - 1]) if not len(bands) % 2 == 0 else None
        desired = np.power(10, interpolation(bands) / 20)
        try:
            self._coeffs = firls(99, bands, desired, fs=44100)
        except Exception as e:
            # todo pop up for communicate user
            Logger.exception(e)
            self._coeffs = None

    def frequency_response(self):
        if self._coeffs is None:
            return []
        freq, response = freqz(self._coeffs, fs=44100)
        ir_points = list(zip(freq + 0.0001, 20 * np.log(np.abs(response))))
        return ir_points

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass

    def phase_response(self):
        pass

    def description(self):
        return """This is test FIR filter. The filter approximate characteristic by
Least-square method. You should add even number of points on graph, because
that method take the points by pair."""

    def menu(self):
        return FilterMenu()

    def process(self, samples):
        if self._coeffs is not None:
            samples = lfilter(self._coeffs.b,
                              self._coeffs.a,
                              samples)
        return samples
