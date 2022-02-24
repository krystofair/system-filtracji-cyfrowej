class BadEntryLine(Exception):
    def __init__(self):
        super().__init__("Bad entry line in filter list's file.")


class IFilter:
    filter_id = None
    filter_kind = ''

    def generate_filter(self, profile):
        raise NotImplementedError

    def load_filter(self, bin_file):
        raise NotImplementedError

    def save_filter(self, path):
        raise NotImplementedError

    def impulse_response(self):
        raise NotImplementedError

    def phase_response(self):
        raise NotImplementedError


# In this place are imports of created filters,
# because every filter should use above interface.
from .test_filter_fir_1 import TestFilterFIR


# list for possibility of iterate by classes
FILTER_LIST = [
    TestFilterFIR
]

__all__ = [
    'FILTER_LIST',
    'TestFilterFIR'
]
