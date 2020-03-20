import re

from livelossplot import MainLogger, PlotLosses


class CheckOutput:
    def send(self, logger: MainLogger):
        assert isinstance(logger, MainLogger)
        grouped_log_history = logger.grouped_log_history(raw_names=True, raw_group_names=True)
        assert len(grouped_log_history) == 2
        assert len(grouped_log_history['accuracy']) == 2
        assert len(grouped_log_history['accuracy']['val_acc']) == 2
        grouped_log_history = logger.grouped_log_history()
        assert len(grouped_log_history) == 2
        assert len(grouped_log_history['accuracy']) == 2
        assert len(grouped_log_history['accuracy']['Validation ']) == 2


def test_plot_losses():
    """Test basic usage"""
    group_patterns = {'accuracy': re.compile(r'.*acc$'), 'log-loss': re.compile(r'.*loss$')}
    loss_plotter = PlotLosses(outputs=(CheckOutput(), ), group_patterns=group_patterns)
    loss_plotter.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    loss_plotter.update({
        'acc': 0.55,
        'loss': 1.1,
    })
    loss_plotter.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    loss_plotter.update({
        'acc': 0.55,
        'loss': 1.1,
    })
    loss_plotter.send()
