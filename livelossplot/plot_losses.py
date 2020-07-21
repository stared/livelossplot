import warnings
from typing import Type, Optional, TypeVar, List

from livelossplot.main_logger import MainLogger
from livelossplot.outputs import BaseOutput, MatplotlibPlot, ExtremaPrinter

BO = TypeVar('BO', bound=BaseOutput)


class PlotLosses:
    """
    Class collect metrics from the training engine and send it to plugins, when send is called
    """
    def __init__(self, outputs: Optional[List[Type[BO]]] = None, mode: str = 'notebook', **kwargs):
        """
        Args:
            outputs: list of callbacks (outputs) which are called with send method
            mode: Options: 'notebook' or 'script' - some of outputs need to change some behaviors,
                depending on the working environment
            **kwargs: key-arguments which are passed to MainLogger constructor
        """
        self.logger = MainLogger(**kwargs)
        self.outputs = outputs if outputs is not None else [MatplotlibPlot(), ExtremaPrinter()]
        for out in self.outputs:
            out.set_output_mode(mode)

    def update(self, *args, **kwargs):
        """update logs with arguments that will be passed to main logger"""
        self.logger.update(*args, **kwargs)

    def send(self):
        """Method will send logs to every output class"""
        for output in self.outputs:
            output.send(self.logger)

    def draw(self):
        """Send method substitute from old livelossplot api"""
        warnings.warn('draw will be deprecated, please use send method', PendingDeprecationWarning)
        self.send()

    def reset_outputs(self) -> 'PlotLosses':
        """Resets all outputs.

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs = []
        return self

    def to_matplotlib(self, *args, **kwargs) -> 'PlotLosses':
        """Appends outputs.MatplotlibPlot output, with specified parameters.

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(MatplotlibPlot(*args, **kwargs))
        return self

    def to_extrema_printer(self, *args, **kwargs) -> 'PlotLosses':
        """Appends outputs.ExtremaPrinter output, with specified parameters.

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(ExtremaPrinter(*args, **kwargs))
        return self
