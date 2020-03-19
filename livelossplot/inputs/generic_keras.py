from livelossplot.plot_losses import PlotLosses


class _PlotLossesCallback:
    """Base keras callback class for keras and tensorflow.keras"""
    def __init__(self, **kwargs):
        self.liveplot = PlotLosses(**kwargs)

    @staticmethod
    def _set_groups(logger, keys):
        if logger.groups or logger.group_patterns:
            return
        groups = {}
        for key in keys:
            abs_key = key.replace('val_', '')
            if not groups.get(abs_key):
                groups[abs_key] = []
            groups[abs_key].append(key)
        logger.groups = groups

    def on_epoch_end(self, epoch, logs):
        """Send metrics to livelossplot"""
        self._set_groups(self.liveplot.logger, logs.keys())
        self.liveplot.update(logs.copy(), epoch)
        self.liveplot.send()
