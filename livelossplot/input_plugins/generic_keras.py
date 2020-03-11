from __future__ import division
from livelossplot.plot_losses import PlotLosses


class _PlotLossesCallback:
    def __init__(self, **kwargs):
        self.liveplot = PlotLosses(**kwargs)

    def on_epoch_end(self, epoch, logs):
        self.liveplot.update(logs.copy(), epoch)
        self.liveplot.send()
