from . import filter_interface

# import list of created filters.
from .test_filter_fir_1 import TestFilterFIR


# list for possibility of iterate by classes
FILTER_LIST = [
    TestFilterFIR
]

__all__ = [
    'FILTER_LIST',
    'TestFilterFIR'
]
