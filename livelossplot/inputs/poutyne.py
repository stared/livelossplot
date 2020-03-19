from poutyne.framework import Callback
from ..plot_losses import PlotLosses


class PlotLossesCallback(Callback):
    """Poutyne is a keras-like api framework for pytorch"""
    def __init__(self, **kwargs):
        """
        :param kwargs: key-word arguments of PlotLosses
        """
        super(PlotLossesCallback, self).__init__()
        self.liveplot = PlotLosses(**kwargs)
        self.metrics = None

    def on_train_begin(self, logs):
        """Create metric names"""
        metrics = ['loss'] + self.model.metrics_names
        self.metrics = list(metrics)
        self.metrics += ['val_' + metric for metric in metrics]

    def on_epoch_end(self, epoch, logs):
        """Send metrics to livelossplot"""
        metric_logs = {metric: logs[metric] for metric in self.metrics if metric in logs}
        self.liveplot.update(metric_logs, epoch)
        self.liveplot.send()
