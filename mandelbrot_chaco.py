import math
import numpy as np

from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import BetterSelectingZoom, PanTool
from enable.api import ComponentEditor
from traits.api import Array, Float, HasStrictTraits, Instance, observe
from traitsui.api import HGroup, UItem, View

from mandel import generate_mandelbrot


class MandelbrotPanTool(PanTool):
    def __init__(self, mandelbrot_plot, component=None, **traits):
        super().__init__(component, **traits)
        self.mandelbrot_plot = mandelbrot_plot

    def dispatch(self, event, suffix):
        super().dispatch(event, suffix)
        if suffix == 'left_up':
            self.mandelbrot_plot.ranges = [
                self.component.x_mapper.range.low,
                self.component.x_mapper.range.high,
                self.component.y_mapper.range.low,
                self.component.y_mapper.range.high
            ]


class MandelbrotBetterSelectingZoom(BetterSelectingZoom):
    def __init__(self, mandelbrot_plot, component=None, **traits):
        super().__init__(component, **traits)
        self.mandelbrot_plot = mandelbrot_plot

    def dispatch(self, event, suffix):
        super().dispatch(event, suffix)
        if event.handled and (
            # pressing 'z' and mouse drag
            suffix == 'left_up'
            # mouse wheel up/down
            or suffix == 'mouse_wheel'
            # shift + up/down/left/right (except pressing 'z')
            or suffix == 'key_pressed' and event.character != 'z'
        ):
            self.mandelbrot_plot.ranges = [
                self._get_x_mapper().range.low,
                self._get_x_mapper().range.high,
                self._get_y_mapper().range.low,
                self._get_y_mapper().range.high
            ]


class MandelbrotPlot(HasStrictTraits):
    ranges = Array(dtype=Float, value=[-2, 1, -1.5, 1.5])
    plot = Instance(Plot)

    def _get_mandelbrot(self):
        x = np.linspace(self.ranges[0], self.ranges[1], num=1000)
        y = np.linspace(self.ranges[2], self.ranges[3], num=1000)
        min_range = min(self.ranges[1] - self.ranges[0], self.ranges[3] - self.ranges[2])
        n = max(int(math.log10(3 / min_range) * 30 + 100), 1)
        return x, y, generate_mandelbrot(x[:-1], y[:-1], n)

    def _plot_default(self):
        x, y, data = self._get_mandelbrot()
        plot = Plot(ArrayPlotData(data=data))
        plot.img_plot('data', xbounds=x, ybounds=y)
        plot.tools.append(MandelbrotPanTool(self, plot))
        plot.overlays.append(MandelbrotBetterSelectingZoom(self, plot, zoom_factor=1.05))
        return plot

    @observe('ranges')
    def _plot_update(self, event):
        x, y, data = self._get_mandelbrot()
        self.plot.data.set_data('data', new_data=data)
        self.plot.img_plot('data', xbounds=x, ybounds=y)

    traits_view = View(
        HGroup(UItem('plot', editor=ComponentEditor())),
        resizable=True,
    )


def main():
    mandelbrot_plot = MandelbrotPlot()
    mandelbrot_plot.configure_traits()


if __name__ == "__main__":
    main()
