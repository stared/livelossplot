from typing import Optional

import ignite.engine
from ignite.handlers import global_step_from_engine
from livelossplot.plot_losses import PlotLosses


class PlotLossesCallback:
    def __init__(self, train_engine: Optional[ignite.engine.Engine] = None, **kwargs):
        """
        :param train_egine - engine with global setep info:
        :param kwargs key-word arguments of PlotLosses:
        """
        self.liveplot = PlotLosses(**kwargs)
        self.train_engine = train_engine

    def attach(self, engine: ignite.engine.Engine):
        """
        Attach callback to ignite engine, attached method will be called on the end of each epoch
         and optionally on the end of every iteration
        """
        engine.add_event_handler(ignite.engine.Events.EPOCH_COMPLETED, self.store)
        engine.add_event_handler(ignite.engine.Events.ITERATION_COMPLETED, self.store)

    def store(self, engine: ignite.engine.Engine):
        """Evaluation engine store state with computed metrics, that will be send to main logger"""
        metrics = {}
        if not hasattr(engine.state, 'metrics') or len(engine.state.metrics) == 0:
            return
        kwargs = dict(
            current_step=global_step_from_engine(self.train_engine)
            (self.train_engine, self.train_engine.last_event_name)
        ) if self.train_engine else {}
        for key, val in engine.state.metrics.items():
            metric_name = key
            metrics[metric_name] = val
        self.liveplot.update(metrics, **kwargs)
        self.liveplot.send()
