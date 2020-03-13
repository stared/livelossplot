import warnings
from typing import Type, Tuple

from livelossplot.main_logger import MainLogger
from livelossplot.output_plugins.base_output import BaseOutput
from livelossplot.output_plugins.matplotlib import Matplotlib
from livelossplot.output_plugins.extrema_print import ExtremaPrint


class PlotLosses:
    """
    Class collect metrics from the training engine and send it to plugins, when send is called
    """

    def __init__(self, outputs: Tuple[Type[BaseOutput]] = (Matplotlib(), ExtremaPrint()), **kwargs):
        """
        :param outputs: list of callbacks (outputs) which are called with send method
        :param kwargs: key-arguments which are passed to main logger
        """
        self.logger = MainLogger(**kwargs)
        self.outputs = outputs

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
