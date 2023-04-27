import numpy as np

from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import BetterSelectingZoom, PanTool
from enable.api import ComponentEditor
from traits.api import Array, Event, Float, HasStrictTraits, Property, observe
from traitsui.api import ButtonEditor, UItem, View

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
    _default_ranges = [-2, 1, -1.5, 1.5]
    ranges = Array(dtype=Float, value=_default_ranges)
    plot = Property(depends_on='ranges')
    reset_zoom = Event

    def _get_plot(self):
        x = np.linspace(self.ranges[0], self.ranges[1], num=1000)
        y = np.linspace(self.ranges[2], self.ranges[3], num=1000)
        plot = Plot(ArrayPlotData(data=generate_mandelbrot(x[:-1], y[:-1], 100)))
        plot.img_plot('data', xbounds=x, ybounds=y)
        plot.tools.append(MandelbrotPanTool(self, plot))
        plot.overlays.append(MandelbrotBetterSelectingZoom(self, plot, zoom_factor=1.05))
        plot.padding_right = plot.padding_top = plot.padding_bottom = 20
        return plot

    @observe('reset_zoom')
    def reset_zoom_pushed(self, event):
        self.ranges = self._default_ranges

    traits_view = View(
        UItem('plot', editor=ComponentEditor()),
        UItem('reset_zoom', editor=ButtonEditor(label='Reset Zoom and Pan')),
        resizable=True,
    )


def main():
    mandelbrot_plot = MandelbrotPlot()
    mandelbrot_plot.configure_traits()


if __name__ == "__main__":
    main()
