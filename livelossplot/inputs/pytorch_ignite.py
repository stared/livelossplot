from typing import Optional

import ignite.engine
from ignite.handlers import global_step_from_engine
from livelossplot.plot_losses import PlotLosses


class PlotLossesCallback:
    def __init__(self, train_engine: Optional[ignite.engine.Engine] = None, **kwargs):
        """
        Args:
            train_engine: engine with global step information, send metohod callback will be attached to it
                if None send method will be called on the end of each store call it may cause warnings and errors in
                the case of multiple engines attached

        Keyword Args:
            **kwargs: keyword args that will be passed to livelossplot PlotLosses class
        """
        self.liveplot = PlotLosses(**kwargs)
        self.train_engine = train_engine
        if self.train_engine:
            self.train_engine.add_event_handler(ignite.engine.Events.EPOCH_STARTED, self.send)
            self.train_engine.add_event_handler(ignite.engine.Events.COMPLETED, self.send)

    def attach(self, engine: ignite.engine.Engine):
        """Attach callback to ignite engine, attached method will be called on the end of each epoch
        Args:
            engine: engine that computes metrics on the end of each epoch and / or on the end of each iteration

        Notes:
            metrics computation plugins have to be attached before this one
        """
        engine.add_event_handler(ignite.engine.Events.EPOCH_COMPLETED, self.store)
        engine.add_event_handler(ignite.engine.Events.ITERATION_COMPLETED, self.store)

    def store(self, engine: ignite.engine.Engine):
        """Store computed metrics, that will be send to main logger
        Args:
            engine: engine with state.metrics
        """
        metrics = {}
        if not hasattr(engine.state, 'metrics') or len(engine.state.metrics) == 0:
            return
        kwargs = dict(
            current_step=global_step_from_engine(self.train_engine)
            (self.train_engine, self.train_engine.last_event_name)
        ) if self.train_engine else {}
        for key, val in engine.state.metrics.items():
            metrics[key] = val
        self.liveplot.update(metrics, **kwargs)
        if not self.train_engine:
            self.send()

    def send(self, _: Optional[ignite.engine.Engine] = None):
        self.liveplot.send()
