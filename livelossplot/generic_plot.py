from __future__ import division
import math

from .core import draw_plot, print_extrema, not_inline_warning, MATPLOTLIB_TARGET, NEPTUNE_TARGET
from collections import OrderedDict

def _is_unset(metric):
    return metric is None or math.isnan(metric) or math.isinf(metric)


class PlotLosses():
    def __init__(self,
                 figsize=None,
                 cell_size=(6, 4),
                 dynamic_x_axis=False,
                 max_cols=2,
                 max_epoch=None,
                 metric2title={},
                 series_fmt={'training': '{}', 'validation':'val_{}'},
                 validation_fmt="val_{}",
                 plot_extrema=True,
                 fig_path=None,
                 target=MATPLOTLIB_TARGET):
        self.figsize = figsize
        self.cell_size = cell_size
        self.dynamic_x_axis = dynamic_x_axis
        self.max_cols = max_cols
        self.max_epoch = max_epoch
        self.metric2title = metric2title
        self.series_fmt = series_fmt
        if validation_fmt is not None:
            # backward compatibility
            self.series_fmt['validation'] = validation_fmt
        self.logs = None
        self.base_metrics = None
        self.metrics_extrema = None
        self.plot_extrema = plot_extrema
        self.target = target
        self._validate_target()
        if target == MATPLOTLIB_TARGET:
            not_inline_warning()
        self.fig_path = fig_path
        self.set_max_epoch(max_epoch)

    def set_max_epoch(self, max_epoch):
        self.max_epoch = max_epoch if not self.dynamic_x_axis else None

    def set_metrics(self, metrics):
        self.base_metrics = metrics
        if self.plot_extrema:
            self.metrics_extrema = {
                ftm.format(metric): {
                    'min': float('inf'),
                    'max': -float('inf'),
                }
                for metric in metrics
                for ftm in list(self.series_fmt.values())
            }
        if self.figsize is None:
            self.figsize = (
                self.max_cols * self.cell_size[0],
                ((len(self.base_metrics) + 1) // self.max_cols + 1) * self.cell_size[1]
            )

        self.logs = []

    def _update_extrema(self, log):
        for metric, value in log.items():
            extrema = self.metrics_extrema[metric]
            if _is_unset(extrema['min']) or value < extrema['min']:
                extrema['min'] = float(value)
            if _is_unset(extrema['max']) or value > extrema['max']:
                extrema['max'] = float(value)

    def update(self, log):
        if self.logs is None:
            self.set_metrics(list(OrderedDict.fromkeys([metric.split('_')[-1] for metric in log.keys()])))
        self.logs.append(log)
        if self.plot_extrema:
            self._update_extrema(log)

    def draw(self):
        if self.target == MATPLOTLIB_TARGET:
            draw_plot(self.logs, self.base_metrics,
                      figsize=self.figsize,
                      max_epoch=self.max_epoch,
                      max_cols=self.max_cols,
                      series_fmt=self.series_fmt,
                      metric2title=self.metric2title,
                      fig_path=self.fig_path)
            if self.metrics_extrema:
                print_extrema(self.logs,
                              self.base_metrics,
                              self.metrics_extrema,
                              series_fmt=self.series_fmt,
                              metric2title=self.metric2title)
        if self.target == NEPTUNE_TARGET:
            from .neptune_integration import neptune_send_plot
            neptune_send_plot(self.logs)

    def _validate_target(self):
        assert isinstance(self.target, str),\
            'target must be str, got "{}" instead.'.format(type(self.target))
        if self.target != MATPLOTLIB_TARGET and self.target != NEPTUNE_TARGET:
            raise ValueError('Target must be "{}" or "{}", got "{}" instead.'.format(MATPLOTLIB_TARGET, NEPTUNE_TARGET, self.target))
