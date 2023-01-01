#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from .filter_interface import IFilter, FilterMenu, FilterUtils
from scipy.interpolate import CubicSpline
from scipy.signal import firls, freqz, filtfilt, lfilter_zi, lfilter
import numpy as np
from kivy.logger import Logger


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'
    options_menu = None

    def __init__(self):
        self.log = Logger
        self._coeffs = None
        self.taps = 99
        self.samples = []
        self.sample_rate = None

    def generate_filter(self, profile):
        points = profile.get_points_as_list()
        if len(points) < 2:
            return
        freqs, amps_dB = zip(*points)
        # XXX Can use interpolation method from profile
        try:
            interpolation = profile.interp_func(freqs, amps_dB)
        except Exception:
            interpolation = CubicSpline(freqs, amps_dB)
        bands = list(range(freqs[0], freqs[len(freqs) - 1]))
        bands.append(bands[len(bands) - 1]) if not len(bands) % 2 == 0 else None
        desired = np.power(10, interpolation(bands) / 20)
        self.sample_rate = FilterUtils.compute_sample_rate(profile)
        try:
            self._coeffs = firls(self.taps, bands, desired, fs=self.sample_rate)
        except Exception as e:
            # todo pop up for communicate user
            Logger.exception(e)
            self._coeffs = None

    def frequency_response(self):
        if self._coeffs is None:
            return []
        fs0 = self.sample_rate if self.sample_rate else 44100
        freq, response = freqz(self._coeffs, fs=fs0)
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

    def process(self, samples_to_process):
        self.samples.extend(samples_to_process)
        processed_samples = lfilter(self._coeffs, np.ones(len(self._coeffs)), self.samples)
        self.samples = self.samples[len(self.samples) - self.taps:]
        return processed_samples

