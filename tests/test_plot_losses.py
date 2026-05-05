from livelossplot import MainLogger, PlotLosses
from livelossplot.outputs import BaseOutput


class CheckOutput(BaseOutput):
    def send(self, logger: MainLogger):
        assert isinstance(logger, MainLogger)
        grouped_log_history = logger.grouped_log_history(raw_names=True, raw_group_names=True)
        assert len(grouped_log_history) == 2
        assert len(grouped_log_history['acc']) == 2
        assert len(grouped_log_history['acc']['val_acc']) == 2
        grouped_log_history = logger.grouped_log_history()
        assert len(grouped_log_history) == 2
        assert len(grouped_log_history['Accuracy']) == 2
        assert len(grouped_log_history['Accuracy']['validation']) == 2


def test_plot_losses():
    """Test basic usage and step counting across heterogeneous updates."""
    loss_plotter = PlotLosses(outputs=[CheckOutput()])
    loss_plotter.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    loss_plotter.update({'acc': 0.55, 'loss': 1.1})
    loss_plotter.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    loss_plotter.update({'acc': 0.55, 'loss': 1.1})
    loss_plotter.send()

    history = loss_plotter.logger.log_history
    assert set(history.keys()) == {'acc', 'val_acc', 'loss', 'val_loss'}
    assert len(history['acc']) == 4
    assert len(history['loss']) == 4
    assert len(history['val_acc']) == 2
    assert len(history['val_loss']) == 2
    assert history['acc'][-1].value == 0.55
    assert history['acc'][-1].step == 3
    assert history['val_acc'][-1].step == 2


def test_plot_losses_to_outputs():
    """to_*() methods chain and return self; reset_outputs clears."""
    plotlosses = PlotLosses(outputs=['MatplotlibPlot'])
    assert len(plotlosses.outputs) == 1
    assert plotlosses.reset_outputs() is plotlosses
    assert plotlosses.outputs == []
    plotlosses.to_matplotlib().to_extrema_printer().to_extrema_printer()
    assert len(plotlosses.outputs) == 3
