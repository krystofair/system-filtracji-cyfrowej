#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
from filters.filter_interface import IFilter
from scipy.io import wavfile
from kivy.logger import Logger


def load_audio_data(path):
    try:
        sample_rate, data = wavfile.read(path)
    except Exception as e:
        Logger.exception(e)
    else:
        return sample_rate, data
    return None


def save_audio_file(path, data, sample_rate):
    wavfile.write(path, sample_rate, data)


def process_samples(data, filter: IFilter = None):
    if filter is None:
        processed_samples = data
    else:
        processed_samples = filter.process(data)
    return processed_samples
