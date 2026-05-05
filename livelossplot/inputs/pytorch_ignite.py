
import ignite.engine
from ignite.handlers import global_step_from_engine

from livelossplot.plot_losses import PlotLosses


class PlotLossesCallback:
    def __init__(self, train_engine: ignite.engine.Engine | None = None, **kwargs):
        """
        Args:
            train_engine: engine with global step information; the send callback will be attached to it.
                If None, send is called at the end of each store call, which may cause warnings or errors
                when multiple engines are attached.

        Keyword Args:
            **kwargs: keyword args forwarded to `PlotLosses`.
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
        """Forward `engine.state.metrics` to the main logger."""
        if not getattr(engine.state, 'metrics', None):
            return
        metrics = dict(engine.state.metrics)
        if self.train_engine is not None:
            step_fn = global_step_from_engine(self.train_engine)
            current_step = step_fn(self.train_engine, self.train_engine.last_event_name)
            self.liveplot.update(metrics, current_step=current_step)
        else:
            self.liveplot.update(metrics)
            self.send()

    def send(self, _: ignite.engine.Engine | None = None) -> None:
        self.liveplot.send()
