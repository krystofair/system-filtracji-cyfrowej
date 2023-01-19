#  Copyright (c) 2023.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
from functools import partial

import numpy as np
from filters.filter import IFilter
from kivy.lang import builder
from scipy.signal import butter, lfilter, freqz
from kivy.logger import Logger


class BandpassButterworthFilter(IFilter):
    filter_id = "BandpassButterWorthFilter"
    filter_kind = "iir"

    def __init__(self):
        self.order = 1
        self.b = []
        self.a = [1]
        self.fs = 44100
        # self.cascade = None

    # def add_to_cascade(self, band_start, band_stop, profile):
    #     if len(profile.get_points_as_list()) < 2 and len(profile.get_points_as_list()) % 2 == 1:
    #         return False
    #     if self.cascade is None:
    #         self.cascade = []
    #     b, a = butter(self.order, [band_start, band_stop], btype='bandpass', output='ba', fs=self.fs)
    #     self.cascade.append(
    #         {
    #             'b': b,
    #             'a': a
    #         }
    #     )
    #     return True

    def generate_filter(self, profile):
        if len(profile.get_points_as_list()) < 2 and len(profile.get_points_as_list()) % 2 == 1:
            return []
        boundary_freq = profile.get_points_as_list()
        band_start, band_stop = boundary_freq[0][0], boundary_freq[-1][0]
        self.b, self.a = butter(self.order, [band_start-19, band_stop], btype='bandpass', output='ba',
                                fs=self.fs)

    @classmethod
    def load_filter(cls, bin_file_or_path):
        pass

    def save_filter(self, path):
        pass

    def frequency_response(self):
        if self.b is None or self.a is None:
            return []
        freq, response = freqz(self.b, self.a, fs=self.fs)
        ir_points = list(zip(freq+20, 20 * np.log(np.abs(response))))
        return ir_points

    def set_order(self, num):
        Logger.info(f'set order to {num}')
        self.order = num

    def phase_response(self):
        super().phase_response()

    def description(self):
        return """
        This is bandpass Butterworth filter as the name suggest. This filter get two points from
        profile, so you have to create only two points, otherwise it take first and last point from
        characteristic. This pair will be treated as boundary of bands to pass.
        These points do not have to be on specific amplitude.
        """
        # """
        # This is bandpass Butterworth filter as the name suggest. This filter get two points from
        # profile as pairs. So you have to prepare even of them. Then each pair will be treated as
        # boundary of bands to pass. These points do not have to be on specific amplitude.
        # On the characteristic there should be at least two points. This class realize butterworth
        # filter connected in cascade.
        # """

    def menu(self):
        return builder.Builder.load_file("gui_menus/bp_bw_filter_menu.kv")

    def process(self, samples, *args, **kwargs):
        channels = len(samples[0])
        return lfilter(self.b, self.a, samples, axis=0)
