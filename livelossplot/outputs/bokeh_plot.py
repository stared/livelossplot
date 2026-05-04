import sys

from livelossplot.main_logger import LogItem, MainLogger
from livelossplot.outputs.base_output import BaseOutput, OutputMode


class BokehPlot(BaseOutput):
    """Simple plugin for a bokeh framework"""
    def __init__(
        self,
        max_cols: int = 2,
        skip_first: int = 2,
        cell_size: tuple[int, int] = (400, 300),
        output_file: str = './bokeh_output.html'
    ):
        """
        Args:
            max_cols: max number of charts in one row
            skip_first: flag, skip first log
            cell_size: size of one chart
            output_file: file to save the output
        """
        from bokeh import io, palettes, plotting
        self.plotting = plotting
        self.io = io
        self.plot_width, self.plot_height = cell_size
        self.max_cols = max_cols
        self.skip_first = skip_first  # think about it
        self.figures = {}
        self.is_notebook = False
        self.is_colab = 'google.colab' in sys.modules
        self.output_file = output_file
        self.colors = palettes.Category10[10]
        self._colab_handle = None

    def send(self, logger: MainLogger) -> None:
        """Draw figures with metrics and show"""
        if self.is_colab:
            self._send_colab(logger)
            return

        log_groups = logger.grouped_log_history()
        new_grid_plot = False
        for _idx, (group_name, group_logs) in enumerate(log_groups.items(), start=1):
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

    def _send_colab(self, logger: MainLogger) -> None:
        """Colab actively blocks Jupyter Comms, so push_notebook is dead there.
        Render Bokeh into a complete HTML doc and embed it via <iframe srcdoc>:
        the iframe is a self-contained browser context, so BokehJS finds its
        sibling JSON-data element correctly (no DOM fragmentation from Colab's
        output handling). Updates via display_id atomically replace the iframe
        wrapper, browser rebuilds the inner document — no flicker."""
        import html as html_lib

        from bokeh.embed import file_html
        from bokeh.resources import CDN
        from IPython.display import HTML, display

        log_groups = logger.grouped_log_history()
        self.figures = {}
        for group_name, group_logs in log_groups.items():
            fig = self.plotting.figure(title=group_name)
            self.figures[group_name] = self._draw_metric_subplot(fig, group_logs)
        rows, row = [], []
        for idx, fig in enumerate(self.figures.values(), start=1):
            row.append(fig)
            if idx % self.max_cols == 0:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
        grid = self.plotting.gridplot(rows, sizing_mode='scale_width', width=self.plot_width, height=self.plot_height)
        bokeh_doc = file_html(grid, CDN, 'livelossplot')
        iframe_height = self.plot_height * len(rows) + 60
        iframe_html = (
            f'<iframe srcdoc="{html_lib.escape(bokeh_doc, quote=True)}" '
            f'style="width: 100%; height: {iframe_height}px; border: none;" '
            f'sandbox="allow-scripts allow-same-origin"></iframe>'
        )
        payload = HTML(iframe_html)
        if self._colab_handle is None:
            self._colab_handle = display(payload, display_id=True)
        else:
            self._colab_handle.update(payload)

    def _draw_metric_subplot(self, fig, group_logs: dict[str, list[LogItem]]):
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
            rows, sizing_mode='scale_width', width=self.plot_width, height=self.plot_height
        )
        self.target = self.plotting.show(self.grid, notebook_handle=self.is_notebook)

    def set_output_mode(self, mode: OutputMode) -> None:
        self.is_notebook = mode == 'notebook'
        if self.is_notebook:
            self.io.output_notebook()
        else:
            self.io.output_file(self.output_file)
