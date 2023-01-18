#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
import io

import kivy
import numpy as np
import store
from kivy.properties import DictProperty, ObjectProperty
from interpolation_funcs import find_id, INTERPOLATION_FUNCTIONS


class NotLoadedProfileException(Exception):
    def __init__(self):
        super().__init__("Profile is not Loaded")


logger = kivy.Logger


class Profile:
    """Interface for guide what properties will be passed in 100% to filter during generation."""
    s_points = DictProperty()  # points on chart which are updating during modifying line.
    interp_func = ObjectProperty()  # Method of interpolation of s_points

    def get_points_as_list(self):
        tmp_points = list(self.s_points.items())
        tmp_points.sort(key=lambda x: x[0])
        return tmp_points

    def save_profile(self, path):
        """
        Profile and others are saved as <count_of_bytes><bytes>.
        The exception is for magic number.
        """
        if not path.endswith('.chr'):
            path = path + ".chr"
        out_file = open(path, 'wb')
        out_file.write(b'CHR0')  # as magic number but on 4 bytes that it is characteristic
        interpolation_func_bytes = find_id(self.interp_func).encode('utf-8')
        out_file.write(len(interpolation_func_bytes).to_bytes(8, 'little'))
        out_file.write(interpolation_func_bytes)
        pts = self.get_points_as_list()
        try:
            x, y = zip(*pts)
            x_bytes, y_bytes = np.array(x).tobytes(), np.array(y).tobytes()
            logger.info(x_bytes)
            logger.info(y_bytes)
            out_file.write(len(x_bytes).to_bytes(8, 'little'))
            out_file.write(x_bytes)
            out_file.write(len(y_bytes).to_bytes(8, 'little'))
            out_file.write(y_bytes)
        except Exception as e:
            logger.error(e)
        finally:
            out_file.close()

    def load_profile(self, path):
        """throws exception(ValueError, EOFError), when loading file failed"""
        in_file = open(path, 'rb')
        if in_file.read(4) != b'CHR0':
            in_file.close()
            raise ValueError("This is not file of profile/characteristic."
                             "Or version of it is wrong.")
        try:
            size = int.from_bytes(in_file.read(8), 'little')
            func_id = in_file.read(size).decode('utf-8')
            try: self.interp_func = INTERPOLATION_FUNCTIONS[func_id]
            except KeyError: self.interp_func = self.interp_func
            store.add_or_update('interpolation-function', func_id)
            size = int.from_bytes(in_file.read(8), 'little')
            x = list(np.frombuffer(in_file.read(size), dtype=int))
            size = int.from_bytes(in_file.read(8), 'little')
            y = list(np.frombuffer(in_file.read(size), dtype=float))
            self.s_points = dict(zip(x, y))
        except EOFError:
            logger.error("There was unexpected end of file.")
        except Exception as e:
            logger.exception(e)
            raise e
        in_file.close()
