import ignite.engine
from livelossplot.generic_plot import PlotLosses


class PlotLossesCallback:
    def __init__(self, metrics_prefix='', **kwargs):
        self.liveplot = PlotLosses(**kwargs)
        self.metrics_prefix = metrics_prefix

    def attach(self, engine):
        engine.add_event_handler(ignite.engine.Events.EPOCH_COMPLETED, self.on_epoch_end)

    def on_epoch_end(self, engine):
        metrics = {}
        for key, val in engine.state.metrics.items():
            metric_name = '{}{}'.format(self.metrics_prefix, key)
            metrics[metric_name] = val
        self.liveplot.update(metrics)
        self.liveplot.draw()
