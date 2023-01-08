#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

from . import filter

# import list of created filters.
from .test_filter_fir_1 import TestFilterFIR
from .test_filter_iir import TestFilterIIR


# list for possibility of iterate by classes
FILTER_LIST = [
    TestFilterFIR,
    TestFilterIIR
]

__all__ = [
    'FILTER_LIST',
    'TestFilterFIR',
    'TestFilterIIR'
]
