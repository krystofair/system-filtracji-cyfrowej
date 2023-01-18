#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.
"""
This is special module to keep interpolation functions in consistent way.
The functions will be take from their IDs, which are keys in dictionary.
Keep those IDs in UTF-8 format, because in conversion to bytes it will be used.
"""
from scipy.interpolate import interp1d, CubicSpline

INTERPOLATION_FUNCTIONS = {
    "cubic": CubicSpline,
    "interp1d": interp1d
}


def find_id(function):
    for key, value in INTERPOLATION_FUNCTIONS.items():
        if value == function:
            return key
    raise Exception("Object Reference Not Set to an Instance of an Object")
