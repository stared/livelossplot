import ignite.engine
from livelossplot.plot_losses import PlotLosses


class PlotLossesCallback:
    def __init__(self, metrics_prefix='', **kwargs):
        """
        :param metrics_prefix: prefix will be added to each metric - f.e. you can add val_ to validation engine
        :param kwargs: key-word arguments of PlotLosses
        """
        self.liveplot = PlotLosses(**kwargs)
        self.metrics_prefix = metrics_prefix

    def attach(self, engine):
        """Attach callback to ignite engine, attached method will be called on the end of each epoch"""
        engine.add_event_handler(ignite.engine.Events.EPOCH_COMPLETED, self.on_epoch_end)

    def on_epoch_end(self, engine):
        """Evaluation engine store state with computed metrics, that will be send to main logger"""
        metrics = {}
        for key, val in engine.state.metrics.items():
            metric_name = '{}{}'.format(self.metrics_prefix, key)
            metrics[metric_name] = val
        self.liveplot.update(metrics)
        self.liveplot.send()
