#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import menus
import store
from kivy.logger import Logger
import soundfile
import wave
import numpy as np
import os

TMP_FILE = 'tmp_processed_file.wav'


def generator_audio_data(path_or_file, blocks=1):
    """
    This function creates generator of blocks as in soundfile module, but additional implementation
    let us decide which type of numpy ndarray we want to use. For now there is serve only for
    PCM_16 (Windows .wav files)
    """
    DEFAULT_ARRAY_TYPE = 'float32'
    if isinstance(path_or_file, str):
        file = soundfile.SoundFile(path_or_file, 'r')
    else:
        file = path_or_file
    if file.subtype == 'PCM_16':
        numpy_array_type = 'h'
    else:
        numpy_array_type = DEFAULT_ARRAY_TYPE

    try:
        while True:
            yield from file.blocks(blocksize=blocks, dtype=numpy_array_type)
    except StopIteration:
        return None
    finally:
        file.close()


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


def try_next(generator):
    try:
        data = next(generator)
    except StopIteration:
        data = []
    return data


def do_block_from_str(string, size):
    result = []
    s = string
    while len(s) > size:
        part1, part2 = s[:size], s[size:]
        result.append(part1)
        s = part2
    if len(s) != 0:
        result.append(s)
    return '\n'.join(result)


def processing_samples(read_path, the_filter, blockrate=1):
    write_path = TMP_FILE
    try:
        read_file = soundfile.SoundFile(read_path, 'r')
    except Exception as e:
        Logger.exception(e)
        store.add_or_update('processing-progress', f'An error occurred during processing')
        store.add_or_update('processing-exception', True)
        return
    write_file = soundfile.SoundFile(write_path, 'w', samplerate=read_file.samplerate,
                                     channels=read_file.channels)
    total_processed_blocks = 0
    BLOCKS = read_file.samplerate * blockrate
    try:
        for samples in read_file.blocks(BLOCKS):
            resampled = the_filter.process(samples)
            write_file.write(resampled)
            total_processed_blocks += 1
            store.update('processing-progress', f"Processed blocks = {total_processed_blocks}\n"
                                                f"One block has {BLOCKS}")
    except Exception as e:
        Logger.exception(e)
        store.add_or_update('processing-progress', do_block_from_str(str(e), 50))
        store.add_or_update('processing-exception', True)
    finally:
        write_file.close()
        read_file.close()
