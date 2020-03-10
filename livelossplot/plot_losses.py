from typing import Type, List

from livelossplot.main_logger import MainLogger
from livelossplot.output_plugins.base_output import BaseOutput
from livelossplot.output_plugins.matplotlib import Matplotlib


class PlotLosses:
    def __init__(self, outputs: List[Type[BaseOutput]] = (Matplotlib(),), **kwargs):
        self.logger = MainLogger(**kwargs)
        self.outputs = outputs

    def update(self, *args, **kwargs):
        self.logger.update(*args, **kwargs)

    def send(self):
        for output in self.outputs:
            output.send(self.logger)
