from pytoune.framework import Callback
from .generic_plot import PlotLosses


class PlotLossesPytoune(Callback):
    def __init__(self, **kwargs):
        super(PlotLossesPytoune, self).__init__()
        self.liveplot = PlotLosses(**kwargs)
        self.metrics = None

    def on_train_begin(self, logs):
        metrics = ['loss'] + self.model.metrics_names
        self.metrics = list(metrics)
        self.metrics += ['val_' + metric for metric in metrics]

    def on_epoch_end(self, epoch, logs):
        metric_logs = {
            metric: logs[metric] for metric in self.metrics
            if metric in logs
        }
        self.liveplot.update(metric_logs)
        self.liveplot.draw()
