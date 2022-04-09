#  Copyright (c) 2022.
#  This file is part of "System Filtracji Cyfrowej", which is released under GPLv2 license.
#  Created by Krzysztof Kłapyta.

import numpy as np
from kivy_garden.graph import LinePlot, ScatterPlot
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from scipy.interpolate import CubicSpline
from kivy.lang import Builder
from profile import Profile


# todo zmienić zoomy na podstawowe dla osi X, a z ctrl dla osi Y
class DesignPlot(LinePlot, Profile):
    """
    Plot shows a line from the set of points, which are according to `interp_func` interpolated
    at full domain. From first two points there is a straight line.
    """
    line_width = NumericProperty(1)
    color = ListProperty([1, 0, 0, 1])
    color2 = ListProperty([1, 1, 1, 1])
    point_size = NumericProperty(3)
    scatter_plot = ObjectProperty()
    interp_func = ObjectProperty(CubicSpline)

    def __init__(self, first_x, last_x, /, point_size=None, color2=None, **kwargs):
        self.color2 = color2 if color2 is not None else self.color2
        self.point_size = self.point_size if point_size is None else point_size
        super().__init__(**kwargs)
        # ustawienie początkowych punktów wykresu
        self.s_points.update({first_x: 0, last_x: 0})
        self.scatter_plot = ScatterPlot(point_size=self.point_size, color=self.color2)
        self.bind(s_points=self.ask_draw)
        self.bind(interp_func=self.ask_draw)
        # self.scatter_plot.bind(points=self.draw)
        # self._interpolate_points() - wykonanie po update punktów

    def get_inner_plot(self):
        return self.scatter_plot

    def _interpolate_points(self):
        tmp_points = self.get_points_as_list()
        if len(tmp_points) >= 2:
            xs, ys = zip(*tmp_points)
            interpolation = self.interp_func(xs, ys)
            rx = range(xs[0], xs[len(xs) - 1])
            self.points = zip(rx, interpolation(rx))
        return tmp_points
        # del xmin, xmax, xs, ys, tmp_points

    def draw(self, *args):
        super().draw(*args)
        points = self._interpolate_points()
        self.scatter_plot.points = points

    def add_point(self, x, y, /):
        self.s_points.update({int(x): round(y, ndigits=2)})

    def remove_point(self, x, /):
        try:
            self.s_points.pop(int(x))
        except:
            pass  # pass cause this is very often and not important.


class FilterPlot(LinePlot):
    """Special class to differentiate a filter plot from others."""
    pass



__all__ = ['DesignPlot', 'FilterPlot']
