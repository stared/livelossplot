from typing import List, Dict, Tuple

from livelossplot.main_logger import MainLogger, LogItem
from livelossplot.outputs.base_output import BaseOutput


class BokehPlot(BaseOutput):
    """Simple plugin for a bokeh framework"""
    def __init__(
        self,
        max_cols: int = 2,
        skip_first: int = 2,
        cell_size: Tuple[int, int] = (600, 400),
        output_file: str = './bokeh_output.html'
    ):
        from bokeh import plotting, io
        self.plotting = plotting
        self.io = io
        self.plot_width, self.plot_height = cell_size
        self.max_cols = max_cols
        self.skip_first = skip_first  # think about it
        self.figures = {}
        self.notebook_handle = False
        self.output_file = output_file

    def send(self, logger: MainLogger) -> None:
        """Draw figures with metrics and show"""
        log_groups = logger.grouped_log_history()
        new_grid_plot = False
        for idx, (group_name, group_logs) in enumerate(log_groups.items(), start=1):
            fig = self.figures.get(group_name)
            if not fig:
                fig = self.plotting.figure(title=group_name)
                new_grid_plot = True
            self.figures[group_name] = self._draw_metric_subplot(fig, group_logs)
        if new_grid_plot:
            self._create_grid_plot()
        if self.notebook_handle:
            self.io.push_notebook(handle=self.target)
        else:
            self.plotting.save(self.grid)

    def _draw_metric_subplot(self, fig, group_logs: Dict[str, List[LogItem]]):
        # for now, with local imports, no output annotation  -> self.plotting.Figure
        # there used to be skip first part, but I skip it first
        for name, logs in group_logs.items():
            if len(logs) > 0:
                xs = [log.step for log in logs]
                ys = [log.value for log in logs]
                fig.line(xs, ys, legend_label=name)
        return fig

    def _create_grid_plot(self):
        rows = []
        row = []
        for idx, fig in enumerate(self.figures.values(), start=1):
            row.append(fig)
            if idx % self.max_cols == 0:
                rows.append(row)
                row = []
        self.grid = self.plotting.gridplot(rows, plot_width=self.plot_width, plot_height=self.plot_height)
        self.target = self.plotting.show(self.grid, notebook_handle=self.notebook_handle)

    def _set_output_mode(self, mode: str):
        """Set notebook or script mode"""
        self.notebook_handle = mode == 'notebook'
        if self.notebook_handle:
            self.io.output_notebook()
        else:
            self.io.output_file(self.output_file)
