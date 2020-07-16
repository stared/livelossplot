from typing import Dict

from poutyne.framework import Callback
from ..plot_losses import PlotLosses


class PlotLossesCallback(Callback):
    """Poutyne is a keras-like api framework for pytorch"""
    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: keyword arguments that will be passed to PlotLosses constructor
        """
        super(PlotLossesCallback, self).__init__()
        self.liveplot = PlotLosses(**kwargs)
        self.metrics = None

    def on_train_begin(self, logs):
        """Create metric names"""
        metrics = ['loss'] + self.model.metrics_names
        self.metrics = list(metrics)
        self.metrics += ['val_' + metric for metric in metrics]

    def on_epoch_end(self, epoch: int, logs: Dict[str, float]):
        """Send metrics to livelossplot
        Args:
            epoch: epoch number
            logs: metrics with values
        """
        metric_logs = {metric: logs[metric] for metric in self.metrics if metric in logs}
        self.liveplot.update(metric_logs, epoch)
        self.liveplot.send()
