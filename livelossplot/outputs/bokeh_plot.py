from typing import List, Dict

from livelossplot.main_logger import MainLogger, LogItem
from livelossplot.outputs.base_output import BaseOutput


class BokehPlot(BaseOutput):
    """Simple plugin for a bokeh framework"""
    def __init__(
        self,
        max_cols: int = 2,
        skip_first: int = 2,
        cell_size: (int, int) = (600, 400),
    ):
        from bokeh import plotting
        self.plotting = plotting
        self.plot_width, self.plot_height = cell_size
        self.max_cols = max_cols
        self.skip_first = skip_first  # think about it

    def send(self, logger: MainLogger) -> None:
        """Draw figures with metrics and show"""
        log_groups = logger.grouped_log_history()
        figures = []
        row = []
        for idx, (group_name, group_logs) in enumerate(log_groups.items(), start=1):
            row.append(self._draw_metric_subplot(group_logs, group_name=group_name))
            if idx % self.max_cols == 0:
                figures.append(row)
                row = []
        grid = self.plotting.gridplot(figures, plot_width=self.plot_width, plot_height=self.plot_height)
        self.plotting.show(grid)

    def _draw_metric_subplot(self, group_logs: Dict[str, List[LogItem]], group_name: str = ''):
        # for now, with local imports, no output annotation  -> self.plotting.Figure
        # there used to be skip first part, but I skip it first
        fig = self.plotting.figure(title=group_name)
        for name, logs in group_logs.items():
            if len(logs) > 0:
                xs = [log.step for log in logs]
                ys = [log.value for log in logs]
                fig.line(xs, ys, legend_label=name)
        return fig
