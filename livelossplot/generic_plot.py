from __future__ import division
import math

from .core import draw_plot, not_inline_warning


def _is_unset(metric):
    return metric is None or math.isnan(metric)


class PlotLosses():
    def __init__(self, figsize=None, cell_size=(6, 4), dynamic_x_axis=False, max_cols=2,
                 max_epoch=None, metric2title={}, validation_fmt="val_{}", plot_extrema=True, fig_path=None):
        self.figsize = figsize
        self.cell_size = cell_size
        self.dynamic_x_axis = dynamic_x_axis
        self.max_cols = max_cols
        self.max_epoch = max_epoch
        self.metric2title = metric2title
        self.validation_fmt = validation_fmt
        self.logs = None
        self.base_metrics = None
        self.metrics_extrema = None
        self.plot_extrema = plot_extrema
        self.fig_path = fig_path

        self.set_max_epoch(max_epoch)
        not_inline_warning()

    def set_max_epoch(self, max_epoch):
        self.max_epoch = max_epoch if not self.dynamic_x_axis else None

    def set_metrics(self, metrics):
        self.base_metrics = metrics
        if self.plot_extrema:
            self.metrics_extrema = {
                ftm.format(metric): {
                    'min': None,
                    'max': None,
                }
                for metric in metrics
                for ftm in ['{}', self.validation_fmt]
            }
        if self.figsize is None:
            self.figsize = (
                self.max_cols * self.cell_size[0],
                ((len(self.base_metrics) + 1) // self.max_cols + 1) * self.cell_size[1]
            )

        self.logs = []

    def _format_metric_name(self, metric_name):
        if 'val' not in metric_name:
            return metric_name
        return metric_name.replace('validation_', 'val_')  # this should be more generic

    def _update_extrema(self, log):
        for metric, value in log.items():
            formatted_name = self._format_metric_name(metric)
            extrema = self.metrics_extrema[formatted_name]
            if _is_unset(extrema['min']) or value < extrema['min']:
                extrema['min'] = float(value)
            if _is_unset(extrema['max']) or value > extrema['max']:
                extrema['max'] = float(value)

    def update(self, log):
        if self.logs is None:
            self.set_metrics([
                metric for metric in log.keys()
                if 'val' not in metric.lower()
            ])
        self.logs.append(log)
        if self.plot_extrema:
            self._update_extrema(log)

    def draw(self):
        draw_plot(self.logs, self.base_metrics,
                  figsize=self.figsize, max_epoch=self.max_epoch,
                  max_cols=self.max_cols,
                  validation_fmt=self.validation_fmt,
                  metric2title=self.metric2title,
                  extrema=self.metrics_extrema,
                  fig_path=self.fig_path)
