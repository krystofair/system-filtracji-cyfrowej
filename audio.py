#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from kivy.logger import Logger
import soundfile
import os


def getting_audio_data(path, frames=100000):
    """
    This generate frames of data from audio file, because file can be too big in size to read at
    once.
    :frames: is how many frame we want to getting from generator.
    """
    try:
        with soundfile.SoundFile(path) as read_snd_file:
            while True:
                data = read_snd_file.read(frames)
                yield data
    except EOFError:
        raise StopIteration
    except Exception as e:
        Logger.exception(e)
        raise StopIteration


def load_audio_data(path):
    try:
        data, _ = soundfile.read(path)
    except Exception as e:
        Logger.exception(e)
    else:
        return data
    return None


def save_audio_file(path, data, sample_rate):
    soundfile.write(path, data, sample_rate)


def create_save_consumer(path, sample_rate, channels=2):
    """
    Function which create consumer for saving continuously processing samples.
    When we invoke `next` on returned consumer then we save this file.
    """
    if os.path.exists(path):
        os.remove(path)

    def saving_data_consumer():
        with soundfile.SoundFile(path, 'x', samplerate=sample_rate, channels=channels) as snd_file:
            while True:
                d = yield
                if d is None:
                    break
                snd_file.write(d)
    c = saving_data_consumer()
    next(c)
    return c


def processing_samples(data, _filter=None):
    """Throw StopIteration"""
    # type(lambda: 0) returns 'function' as a type.
    if issubclass(type(data), type(lambda: 0)):
        data_iterator = iter(data())
    else:
        data_iterator = iter(data)
    while True:
        d = next(data_iterator)
        if _filter is None:
            processed_samples = d
        else:
            processed_samples = _filter.process(d)
        yield processed_samples
