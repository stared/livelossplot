from typing import List, Dict, Tuple

from livelossplot.main_logger import MainLogger, LogItem
from livelossplot.outputs.base_output import BaseOutput


class BokehPlot(BaseOutput):
    """Simple plugin for a bokeh framework"""
    def __init__(
        self,
        max_cols: int = 2,
        skip_first: int = 2,
        cell_size: Tuple[int, int] = (400, 300),
        output_file: str = './bokeh_output.html'
    ):
        """
        Args:
            max_cols: max number of charts in one row
            skip_first: flag, skip first log
            cell_size: size of one chart
            output_file: file to save the output
        """
        from bokeh import plotting, io, palettes
        self.plotting = plotting
        self.io = io
        self.plot_width, self.plot_height = cell_size
        self.max_cols = max_cols
        self.skip_first = skip_first  # think about it
        self.figures = {}
        self.is_notebook = False
        self.output_file = output_file
        self.colors = palettes.Category10[10]

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
        if self.is_notebook:
            self.io.push_notebook(handle=self.target)
        else:
            self.plotting.save(self.grid)

    def _draw_metric_subplot(self, fig, group_logs: Dict[str, List[LogItem]]):
        """
        Args:
            fig: bokeh Figure
            group_logs: groups with list of log items

        Notes:
            for now, with local imports, no output annotation  -> self.plotting.Figure
            there used to be skip first part, but I skip it first
        """
        from bokeh.models import ColumnDataSource, HoverTool
        for i, (name, logs) in enumerate(group_logs.items()):
            if len(logs) > 0:
                source = ColumnDataSource(
                    data={
                        'step': [log.step for log in logs],
                        'value': [log.value for log in logs],
                    }
                )
                fig.line(x='step', y='value', color=self.colors[i], legend_label=name, source=source)

        fig.add_tools(
            HoverTool(
                tooltips=[
                    ('step', '@step'),
                    ('value', '@value{0.3f}'),
                ],
                formatters={
                    'step': 'printf',
                    'value': 'printf',
                },
                mode='vline'
            )
        )
        return fig

    def _create_grid_plot(self):
        rows = []
        row = []
        for idx, fig in enumerate(self.figures.values(), start=1):
            row.append(fig)
            if idx % self.max_cols == 0:
                rows.append(row)
                row = []
        self.grid = self.plotting.gridplot(
            rows, sizing_mode='scale_width', plot_width=self.plot_width, plot_height=self.plot_height
        )
        self.target = self.plotting.show(self.grid, notebook_handle=self.is_notebook)

    def _set_output_mode(self, mode: str):
        """Set notebook or script mode"""
        self.is_notebook = mode == 'notebook'
        if self.is_notebook:
            self.io.output_notebook()
        else:
            self.io.output_file(self.output_file)
