from __future__ import absolute_import

from pytoune.framework import Callback
from .generic_plot import PlotLosses


class PlotLossesCallback(Callback):
    def __init__(self, **kwargs):
        super(PlotLossesCallback, self).__init__()
        self.liveplot = PlotLosses(**kwargs)
        self.metrics = None
        self.samples_per_update = kwargs["samples_per_update"] if "samples_per_update" in kwargs else None

    def on_train_begin(self, logs):
        metrics = ['loss'] + self.model.metrics_names
        self.metrics = list(metrics)
        self.metrics += ['val_' + metric for metric in metrics]
        self.liveplot.set_max_epoch(self.params['epochs'])

    def on_epoch_end(self, epoch, logs):
        metric_logs = {
            metric: logs[metric] for metric in self.metrics
            if metric in logs
        }
        self.liveplot.update(metric_logs)
        self.liveplot.draw()
    def on_batch_end(self, epoch, logs):
        self.liveplot.update(logs.copy(), epoch_log = False)
        if self.samples_per_update is not None:
            self.liveplot.draw()
