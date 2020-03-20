from livelossplot.plot_losses import PlotLosses


class _PlotLossesCallback:
    """Base keras callback class for keras and tensorflow.keras"""
    def __init__(self, **kwargs):
        self.liveplot = PlotLosses(**kwargs)

    def on_epoch_end(self, epoch, logs):
        """Send metrics to livelossplot"""
        self.liveplot.update(logs.copy(), epoch)
        self.liveplot.send()
