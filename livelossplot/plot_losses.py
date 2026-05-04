from typing import TypeVar

import livelossplot
from livelossplot import outputs
from livelossplot.main_logger import MainLogger
from livelossplot.outputs.base_output import OutputMode
from livelossplot.outputs.matplotlib_plot import MatplotlibPlot

BO = TypeVar('BO', bound=outputs.BaseOutput)


def get_mode() -> OutputMode:
    """Detect whether we're running in a notebook (Jupyter, Colab) or a script."""
    try:
        from IPython import get_ipython
    except ImportError:
        return 'script'
    ipython = get_ipython()
    if ipython is None:
        return 'script'
    # ZMQInteractiveShell: Jupyter; Shell: Colab; TerminalInteractiveShell: ipython REPL.
    return 'notebook' if ipython.__class__.__name__ in {'ZMQInteractiveShell', 'Shell'} else 'script'


class PlotLosses:
    """Collect training metrics and dispatch them to one or more output plugins."""

    def __init__(
        self,
        outputs: list[type[BO] | str] | None = None,
        mode: OutputMode | None = None,
        figsize: tuple[int, int] | None = None,
        **kwargs,
    ):
        """
        Args:
            outputs: list of output instances (subclasses of `BaseOutput`) or string names of built-in
                outputs to instantiate with defaults. Defaults to `['MatplotlibPlot', 'ExtremaPrinter']`.
            mode: 'notebook' or 'script'. Auto-detected if `None`.
            figsize: `(width, height)` in inches; applies to `MatplotlibPlot` outputs.
            **kwargs: forwarded to `MainLogger`.
        """
        if outputs is None:
            outputs = ['MatplotlibPlot', 'ExtremaPrinter']
        self.logger = MainLogger(**kwargs)
        self.outputs = [getattr(livelossplot.outputs, out)() if isinstance(out, str) else out for out in outputs]
        if mode is None:
            mode = get_mode()
        for out in self.outputs:
            out.set_output_mode(mode)
            if figsize is not None and isinstance(out, MatplotlibPlot):
                out.figsize = figsize

    def update(self, *args, **kwargs) -> None:
        """Forward to `MainLogger.update`."""
        self.logger.update(*args, **kwargs)

    def send(self) -> None:
        """Send the current logs to every output plugin."""
        for output in self.outputs:
            output.send(self.logger)

    def reset_outputs(self) -> 'PlotLosses':
        """Drop all outputs (chainable)."""
        self.outputs = []
        return self

    def to_matplotlib(self, **kwargs) -> 'PlotLosses':
        """Append a `MatplotlibPlot` output (chainable)."""
        self.outputs.append(outputs.MatplotlibPlot(**kwargs))
        return self

    def to_extrema_printer(self, **kwargs) -> 'PlotLosses':
        """Append an `ExtremaPrinter` output (chainable)."""
        self.outputs.append(outputs.ExtremaPrinter(**kwargs))
        return self

    def to_bokeh(self, **kwargs) -> 'PlotLosses':
        """Append a `BokehPlot` output (chainable)."""
        self.outputs.append(outputs.BokehPlot(**kwargs))
        return self

    def to_tensorboard(self, **kwargs) -> 'PlotLosses':
        """Append a `TensorboardLogger` output (chainable)."""
        self.outputs.append(outputs.TensorboardLogger(**kwargs))
        return self

    def to_tensorboard_tf(self, **kwargs) -> 'PlotLosses':
        """Append a `TensorboardTFLogger` output (chainable)."""
        self.outputs.append(outputs.TensorboardTFLogger(**kwargs))
        return self
