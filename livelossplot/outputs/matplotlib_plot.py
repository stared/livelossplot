from typing import Tuple, List, Dict, Optional, Callable

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
        cell_size: Tuple[int, int] = (6, 4),
        max_cols: int = 2,
        max_epoch: int = None,
        skip_first: int = 2,
        extra_plots: List[Callable[[MainLogger], None]] = [],
        figpath: Optional[str] = None,
        after_subplot: Optional[Callable[[str, str], None]] = None,
        before_plots: Optional[Callable[[int], None]] = None,
        after_plots: Optional[Callable[[], None]] = None,
    ):
        """
        :param cell_size size of one chart:
        :param max_cols maximal number of charts in one row:
        :param max_epoch maximum epoch on x axis:
        :param skip_first number of first steps to skip:
        :param extra_plots extra charts functions:
        :param figpath path to save figure:
        :param after_subplot function which will be called after every subplot:
        :param before_plots function which will be called before all subplots:
        :param after_plots function which will be called after all subplots:
        """
        self.cell_size = cell_size
        self.max_cols = max_cols
        self.skip_first = skip_first  # think about it
        self.extra_plots = extra_plots
        self.max_epoch = max_epoch
        self.figpath = figpath
        self.file_idx = 0  # now only for saving files
        self._after_subplot = after_subplot if after_subplot else self._default_after_subplot
        self._before_plots = before_plots if before_plots else self._default_before_plots
        self._after_plots = after_plots if after_plots else self._default_after_plots

    def send(self, logger: MainLogger):
        """Draw figures with metrics and show"""
        log_groups = logger.grouped_log_history()

        max_rows = (len(log_groups) + len(self.extra_plots) + 1) // self.max_cols + 1

        clear_output(wait=True)
        self._before_plots(len(log_groups))

        for group_idx, (group_name, group_logs) in enumerate(log_groups.items()):
            plt.subplot(max_rows, self.max_cols, group_idx + 1)
            self._draw_metric_subplot(
                group_logs, group_name=group_name, x_label=logger.step_names.get(group_name, 'epoch')
            )

        for idx, extra_plot in enumerate(self.extra_plots):
            plt.subplot(max_rows, self.max_cols, idx + len(log_groups) + 1)
            extra_plot(logger)

        self._after_plots()
        if self.figpath is not None:
            plt.savefig(self.figpath.format(i=self.file_idx))
            self.file_idx += 1

        plt.show()

    def _default_after_subplot(self, group_name: str, x_label: str):
        """Add title xlabel and legend to single chart"""
        plt.title(group_name)
        plt.xlabel(x_label)
        plt.legend(loc='center right')

    def _default_before_plots(self, num_of_log_groups: int) -> None:
        """Set matplotlib window properties"""
        figsize_x = self.max_cols * self.cell_size[0]
        figsize_y = ((num_of_log_groups + 1) // self.max_cols + 1) * self.cell_size[1]
        plt.figure(figsize=(figsize_x, figsize_y))

    def _default_after_plots(self):
        """Set properties after charts creation"""
        plt.tight_layout()

    def _draw_metric_subplot(self, group_logs: Dict[str, List[LogItem]], group_name: str, x_label: str):
        # there used to be skip first part, but I skip it first
        if self.max_epoch is not None:
            plt.xlim(0, self.max_epoch)

        for name, logs in group_logs.items():
            if len(logs) > 0:
                xs = [log.step for log in logs]
                ys = [log.value for log in logs]
                plt.plot(xs, ys, label=name)

        self._after_subplot(group_name, x_label)

    def _not_inline_warning(self):
        backend = matplotlib.get_backend()
        if "backend_inline" not in backend:
            warnings.warn(
                "livelossplot requires inline plots.\nYour current backend is: {}"
                "\nRun in a Jupyter environment and execute '%matplotlib inline'.".format(backend)
            )
