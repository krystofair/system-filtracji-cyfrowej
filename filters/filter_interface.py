class BadEntryLine(Exception):
    def __init__(self):
        super().__init__("Bad entry line in filter list's file.")


class IFilter:
    filter_id = None  # id in ASCII to identify filter in program and further in file.
    filter_kind = ''  # part of filter name showed after '#' (FIR or IIR) to inform user.

    def generate_filter(self, profile):
        """Method which will be called for compute coefficients of filters
        in their internal representation. This method can be called in thread (executor).
        Args:
            profile: Look at `Profile` class to see what field it contain.
        """
        raise NotImplementedError

    def load_filter(self, bin_file):
        """Method used to load internal representation of filter,
        Args:
            bin_file: binary file from filter can be loaded, this file has checked by id before pass to.
        """
        raise NotImplementedError

    def save_filter(self, path):
        """
        This method will be call when user want to save designed filter,
        so class of filter should know how to
        Parameters
        ----------
        path

        Returns
        -------

        """
        raise NotImplementedError

    def frequency_response(self):
        """Should return points in sorted list of (x, y) to feed
        plot with them."""
        raise NotImplementedError

    def phase_response(self):
        """Same as impulse_response."""
        raise NotImplementedError

    def description(self):
        """Filter description in order to user can find out the internals,
        what is interpolation of points in that filter, so user can
        choose right method of interpolation profile.
        See class `TestFilterFIR` to see how to return string,
        which will be nice displayed."""
        return ''

    def menu(self):
        """Return generated menu as `ContextMenu` widget for filter parameters.
        This is simpler approach than passes a parameters and generate filter in
        another method."""
        return None
