import warnings
from typing import Type, TypeVar, List, Union

import livelossplot
from livelossplot.main_logger import MainLogger
from livelossplot import outputs

BO = TypeVar('BO', bound=outputs.BaseOutput)


class PlotLosses:
    """
    Class collect metrics from the training engine and send it to plugins, when send is called
    """
    def __init__(
        self,
        outputs: List[Union[Type[BO], str]] = ['MatplotlibPlot', 'ExtremaPrinter'],
        mode: str = 'notebook',
        **kwargs
    ):
        """
        Args:
            outputs: list of output modules: objects inheriting from BaseOutput
                or strings for livelossplot built-in output methods with default parameters
            mode: Options: 'notebook' or 'script' - some of outputs need to change some behaviors,
                depending on the working environment
            **kwargs: key-arguments which are passed to MainLogger constructor
        """
        self.logger = MainLogger(**kwargs)
        self.outputs = [getattr(livelossplot.outputs, out)() if isinstance(out, str) else out for out in outputs]
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

    def to_matplotlib(self, **kwargs) -> 'PlotLosses':
        """Appends outputs.MatplotlibPlot output, with specified parameters.

        Args:
            **kwargs: keyword arguments for MatplotlibPlot

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(outputs.MatplotlibPlot(**kwargs))
        return self

    def to_extrema_printer(self, **kwargs) -> 'PlotLosses':
        """Appends outputs.ExtremaPrinter output, with specified parameters.

        Args:
            **kwargs: keyword arguments for ExtremaPrinter

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(outputs.ExtremaPrinter(**kwargs))
        return self

    def to_bokeh(self, **kwargs) -> 'PlotLosses':
        """Appends outputs.BokehPlot output, with specified parameters.

        Args:
            **kwargs: keyword arguments for BokehPlot

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(outputs.BokehPlot(**kwargs))
        return self

    def to_neptune(self, **kwargs) -> 'PlotLosses':
        """Appends outputs.NeptuneLogger output, with specified parameters.

        Args:
            **kwargs: keyword arguments for NeptuneLogger

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(outputs.NeptuneLogger(**kwargs))
        return self

    def to_tensorboard(self, **kwargs) -> 'PlotLosses':
        """Appends outputs.TensorboardLogger output, with specified parameters.

        Args:
            **kwargs: keyword arguments for TensorboardLogger

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(outputs.TensorboardLogger(**kwargs))
        return self

    def to_tensorboard_tf(self, **kwargs) -> 'PlotLosses':
        """Appends outputs.TensorboardTFLogger output, with specified parameters.

        Args:
            **kwargs: keyword arguments for TensorboardTFLogger

        Returns:
            Plotlosses object (so it works for chaining)
        """
        self.outputs.append(outputs.TensorboardTFLogger(**kwargs))
        return self
