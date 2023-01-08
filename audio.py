#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import store
from kivy.logger import Logger
import soundfile
import os


def generator_audio_data(path, frames=1000000):
    """
    This generate frames of data from audio file, because file can be too big in size to read at
    once.
    :frames: is how many frame we want to getting from generator.
    """
    try:
        with soundfile.SoundFile(path) as read_snd_file:
            all_frames = read_snd_file.frames
            while all_frames > 0:
                count_frames = frames if all_frames - frames >= 0 else all_frames
                data = read_snd_file.read(count_frames)
                all_frames -= count_frames
                yield data
    except Exception as e:
        Logger.exception(e)


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


def create_save_consumer(path, sample_rate, channels):
    """
    Function which create consumer for saving continuously processing samples.
    When we invoke `next` on returned consumer then we save this file.
    """
    if os.path.exists(path):
        os.remove(path)

    def saving_data_consumer():
        with soundfile.SoundFile(path, 'w', samplerate=sample_rate, channels=channels) as snd_file:
            while True:
                d = yield
                if d is None:
                    break
                snd_file.write(d)

    c = saving_data_consumer()
    next(c)  # initialize consumer
    return c


def processing_samples(read_generator, write_generator, the_filter):
    try:
        percent = 0
        while True:
            samples = next(read_generator)
            processed_samples = the_filter.process(samples)
            write_generator.send(processed_samples)
            percent += 1 if percent < 100 else 100
            store.add_or_update('processing-progress', f"{percent}%")
    except StopIteration:
        write_generator.send(None)
