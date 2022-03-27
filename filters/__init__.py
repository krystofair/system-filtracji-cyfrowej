from . import filter_interface

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
