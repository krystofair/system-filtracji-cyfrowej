#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from collections import deque

import numpy as np
from kivy.logger import Logger
from scipy.interpolate import CubicSpline
from scipy.signal import firls, freqz, lfilter

from .filter import IFilter, FilterMenu, FilterUtils


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'
    options_menu = None

    def __init__(self):
        self.log = Logger
        self._coeffs = None  # aka. numerator coefficients
        self.taps = 99
        self.samples = deque(maxlen=self.taps*2)
        self.state = None
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
        if not self.sample_rate:
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
        ir_points = list(zip(freq, 20 * np.log(np.abs(response))))
        return ir_points

    @classmethod
    def load_filter(cls, binfile_or_path):
        if isinstance(binfile_or_path, str):
            file = open(binfile_or_path, 'rb')
        else:
            file = binfile_or_path
        if b'FIL8' != file.read(len(b'FIL8')):
            raise Exception("This file is not compatible version of filter file")
        filter_id_len = int.from_bytes(file.read(8), 'little')
        filter_id = file.read(filter_id_len).decode('utf-8')
        if filter_id != cls.filter_id:
            raise Exception(f"From file {file.name} cannot create filter {cls.filter_id}.")
        this = cls()
        count_of_coeffs = int.from_bytes(file.read(16), 'little')
        this._coeffs = np.frombuffer(file.read(count_of_coeffs))
        return this

    def save_filter(self, path):
        """
        Profile and others are saved as <count_of_bytes><bytes>.
        The exception is for magic number.
        """
        if self._coeffs is not None:
            out_file = open(path, 'wb')
            out_file.write(b'FIL8')  # as magic number but on 4 bytes that it is characteristic
            # here will be bug if the filter_id is out of bounds eight bytes.
            # but 8 bytes imply 8*8 = 64 bits so this should be enough
            out_file.write(len(self.filter_id).to_bytes(8, 'little'))
            out_file.write(self.filter_id.encode('utf-8'))
            out_file.write(len(self._coeffs.dtype).to_bytes(16, 'little'))
            out_file.write(self._coeffs)
            out_file.close()

    def phase_response(self):
        pass

    def description(self):
        return """This is test FIR filter. The filter approximate characteristic by
Least-square method. You should add even number of points on graph, because
that method take the points by pair."""

    def menu(self):
        return FilterMenu()

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    def process(self, samples_to_process, *args, **kwargs):
        denominator_a = np.zeros(len(self._coeffs)-1)
        denominator_a[0] = 1
        ps = lfilter(self._coeffs, denominator_a, samples_to_process, axis=0)
        return ps

