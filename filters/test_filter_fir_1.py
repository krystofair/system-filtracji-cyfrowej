from . import IFilter


class TestFilterFIR(IFilter):
    filter_id = 'TeStFiLtEr'
    filter_kind = 'fir'

    def __init__(self):
        self._coeffs = []

    def generate_filter(self, profile):
        pass

    def load_filter(self, bin_file):
        pass

    def save_filter(self, path):
        pass