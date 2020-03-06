from typing import List
from main_logger import MainLogger

class PlotLosses:
    def __init__(self, outputs=['tensorboard', 'extrema']):
        self.logger = MainLogger()
        self.outputs = []

    def update(self, *args, **kwargs):
        self.logger.update(*args, **kwargs)

    def send(self):
        for output in self.outputs:
            output.send(self.logger)

