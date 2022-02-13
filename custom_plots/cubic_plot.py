from kivy_garden.graph import MeshLinePlot
from scipy.interpolate import CubicSpline

class CubicPlot(MeshLinePlot):

    def plot_mesh(self):
        points = [p for p in self.iterate_points()]
        cs = CubicSpline(points)

