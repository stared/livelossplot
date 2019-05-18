from __future__ import division
import warnings

from IPython.display import clear_output

from bokeh.plotting import figure, save
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import gridplot
from bokeh.models import Range1d

from bokeh.models import HoverTool

BOKEH_TARGET = 'bokeh'
COLORS = [(31, 119, 180), (255, 165, 0), (46, 139, 87)]
TOOLTIPS = [
    ("Epoch", "@x"),
    ("Value", "@y"),
]


class BokehPlot():

    def __init__(self,
                 logs=None,
                 metrics=None,
                 figsize=[400, 300],
                 max_epoch=None,
                 max_cols=2,
                 series_fmt={'training': '{}', 'validation': 'val_{}'},
                 metric2title={},
                 extra_plots=[],
                 fig_path=None,
                 figures=None,
                 target=None,
                 grid=None):

        self.logs = logs
        self.metrics = metrics
        self.figsize = figsize
        self.max_epoch = max_epoch
        self.max_cols = max_cols
        self.series_fmt = series_fmt
        self.metric2title = metric2title
        self.extra_plots = extra_plots
        self.fig_path = fig_path

        self.figures = figures
        self.target = target
        self.grid = grid

    def create_figures(self):

        output_notebook(hide_banner=True)

        if self.max_epoch:
            x_range = (1, self.max_epoch)
        else:
            x_range = None

        self.figures = []

        for _, metric in enumerate(self.metrics):
            fig = figure(title=metric,
                         x_axis_label='epoch',
                         tools=['hover,pan,wheel_zoom,box_zoom,reset'],
                         tooltips=TOOLTIPS,
                         plot_width=self.figsize[0],
                         plot_height=self.figsize[1],
                         x_range=x_range)
            line = fig.line(x=1, y=1)
            fig.title.text = str(metric)

            hover = HoverTool(tooltips=[("x", "@x"), ("y", "@y")])
            fig.add_tools(hover)

            fig.grid.visible = False
            self.figures.append(fig)

        self.grid = gridplot(self.figures, ncols=self.max_cols)
        self.target = show(self.grid, notebook_handle=True)

    def draw_plot(self,
                  logs,
                  metrics,
                  figsize=None,
                  max_epoch=None,
                  max_cols=2,
                  series_fmt={'training': '{}', 'validation': 'val_{}'},
                  metric2title={},
                  extra_plots=[],
                  fig_path=None):

        for _, metric in enumerate(self.metrics):
            for i, (serie_label, serie_fmt) in enumerate(self.series_fmt.items()):
                if serie_fmt.format(metric) in logs[0]:

                    serie_metric_name = serie_fmt.format(metric)
                    serie_metric_logs = [log[serie_metric_name]
                                         for log in logs]
                    # REMEMBER you have to specify the fig among figures list.
                    # line = self.figures[_].line(range(1, len(logs) + 1), serie_metric_logs,
                    #                             )

                    self.figures[_].line(range(1, len(logs) + 1),
                                         serie_metric_logs, legend=serie_label, line_width=2, color=COLORS[i])
                    self.figures[_].title.text = str(metric)

                    self.figures[_].legend.location = "center_right"
                    self.figures[_].legend.background_fill_alpha = 0.5
                    self.figures[_].legend.padding = 5
                    self.figures[_].xaxis.ticker = [
                        i for i in range(1, len(logs)+1)]

                    self.figures[_].add_tools(HoverTool(tooltips=[
                        ("Epoch", "@x"),
                        ("Value", "@y"),
                    ]
                    ))
        push_notebook(handle=self.target)

        if self.fig_path:
            save(self.grid, filename=fig_path)
