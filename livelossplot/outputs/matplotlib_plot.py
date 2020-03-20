from typing import List

import warnings

import matplotlib
import matplotlib.pyplot as plt
from IPython.display import clear_output
from livelossplot.main_logger import MainLogger, LogItem
from livelossplot.outputs.base_output import BaseOutput


class MatplotlibPlot(BaseOutput):
    """NOTE: Removed figsize and dynamix_x_axis."""
    def __init__(
        self,
        cell_size: (int, int) = (6, 4),
        max_cols: int = 2,
        max_epoch: int = None,
        skip_first: int = 2,
        extra_plots=[],
        figpath: str or None = None
    ):
        self.cell_size = cell_size
        self.max_cols = max_cols
        self.max_epoch = max_epoch
        self.skip_first = skip_first  # think about it
        self.extra_plots = extra_plots
        self.max_epoch = max_epoch
        self.figpath = figpath
        self.file_idx = 0  # now only for saving files

    def send(self, logger: MainLogger):
        """Draw figures with metrics and show"""
        log_groups = logger.grouped_log_history()
        figsize_x = self.max_cols * self.cell_size[0]
        figsize_y = ((len(log_groups) + 1) // self.max_cols + 1) * self.cell_size[1]

        max_rows = (len(log_groups) + len(self.extra_plots) + 1) // self.max_cols + 1

        clear_output(wait=True)
        plt.figure(figsize=(figsize_x, figsize_y))

        for group_id, (group_name, group_logs) in enumerate(log_groups.items()):
            plt.subplot(max_rows, self.max_cols, group_id + 1)
            self._draw_metric_subplot(group_logs, group_name=group_name)

        for i, extra_plot in enumerate(self.extra_plots):
            plt.subplot(max_rows, self.max_cols, i + len(log_groups) + 1)
            extra_plot(logger)

        plt.tight_layout()
        if self.figpath is not None:
            plt.savefig(self.figpath.format(i=self.file_idx))
            self.file_idx += 1
        plt.show()

    def _draw_metric_subplot(self, group_logs: List[LogItem], group_name: str = ''):
        # there used to be skip first part, but I skip it first
        if self.max_epoch is not None:
            plt.xlim(0, self.max_epoch)

        for name, logs in group_logs.items():
            if len(logs) > 0:
                xs = [log.step for log in logs]
                ys = [log.value for log in logs]
                plt.plot(xs, ys, label=name)

        plt.title(group_name)
        plt.xlabel('epoch')
        plt.legend(loc='center right')

    def _not_inline_warning(self):
        backend = matplotlib.get_backend()
        if "backend_inline" not in backend:
            warnings.warn(
                "livelossplot requires inline plots.\nYour current backend is: {}"
                "\nRun in a Jupyter environment and execute '%matplotlib inline'.".format(backend)
            )
