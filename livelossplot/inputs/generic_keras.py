from typing import Dict

from livelossplot.plot_losses import PlotLosses


class _PlotLossesCallback:
    """Base keras callback class for keras and tensorflow.keras"""
    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: keyword arguments that will be passed to PlotLosses constructor
        """
        self.liveplot = PlotLosses(**kwargs)

    def on_epoch_end(self, epoch: int, logs: Dict[str, float]):
        """Send metrics to livelossplot
        Args:
            epoch: epoch number
            logs: metrics with values
        """
        self.liveplot.update(logs.copy(), epoch)
        self.liveplot.send()
