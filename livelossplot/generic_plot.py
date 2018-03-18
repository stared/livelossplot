from __future__ import division

from .core import draw_plot

class PlotLosses():
    def __init__(self, figsize=None, cell_size=(6, 4), dynamic_x_axis=False, max_cols=2, max_epoch=None, metric2title={},
    validation_fmt="val_{}"):
        self.figsize = figsize
        self.cell_size = cell_size
        self.dynamic_x_axis = dynamic_x_axis
        self.max_cols = max_cols
        self.max_epoch = max_epoch
        self.metric2title = metric2title
        self.validation_fmt = validation_fmt
        self.logs = None

    def set_metrics(self, metrics):
        self.base_metrics = metrics
        if self.figsize is None:
            self.figsize = (
                self.max_cols * self.cell_size[0],
                ((len(self.base_metrics) + 1) // self.max_cols + 1) * self.cell_size[1]
            )

        self.logs = []

    def update(self, log):
        if self.logs is None:
            self.set_metrics([metric for metric in log.keys() if not 'val' in metric.lower()])
        self.logs.append(log)

    def draw(self):
        draw_plot(self.logs, self.base_metrics,
                  figsize=self.figsize, max_epoch=self.max_epoch,
                  max_cols=self.max_cols,
                  validation_fmt=self.validation_fmt,
                  metric2title=self.metric2title)
