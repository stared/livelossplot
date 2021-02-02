from livelossplot import MainLogger, PlotLosses
from livelossplot.outputs import BaseOutput


class CheckOutput(BaseOutput):
    def __init__(self, target_log_history_length):
        self.target_log_history_length = target_log_history_length

    def send(self, logger: MainLogger):
        grouped_log_history = logger.grouped_log_history()
        for group, metrics in grouped_log_history.items():
            for metric, logs in metrics.items():
                if len(logs) != self.target_log_history_length:
                    raise ValueError(f'History too long ({len(logs)}) for {group} {metric}')


def test_plus_from_step():
    """Test from_step > 0"""
    out = CheckOutput(target_log_history_length=8)
    loss_plotter = PlotLosses(outputs=[out], from_step=2)
    for idx in range(10):
        loss_plotter.update({
            'acc': 0.1 * idx,
            'loss': 0.69 / (idx + 1),
        })
    loss_plotter.send()


def test_minus_from_step():
    """Test from_step < 0"""
    out = CheckOutput(target_log_history_length=6)
    loss_plotter = PlotLosses(outputs=[out], from_step=-5)
    for idx in range(10):
        loss_plotter.update({
            'acc': 0.1 * idx,
            'loss': 0.69 / (idx + 1),
        })
    loss_plotter.send()


def test_default_from_step():
    """Test without from_step"""
    out = CheckOutput(target_log_history_length=10)
    loss_plotter = PlotLosses(outputs=[out])
    for idx in range(10):
        loss_plotter.update({
            'acc': 0.1 * idx,
            'loss': 0.69 / (idx + 1),
        })
    loss_plotter.send()
