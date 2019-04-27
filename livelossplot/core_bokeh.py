from __future__ import division
import warnings

from IPython.display import clear_output

from bokeh.plotting import figure, reset_output, save
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import gridplot
from bokeh.models import Range1d


BOKEH_TARGET = 'bokeh'
COLORS = [(31, 119, 180), (255, 165, 0), (46, 139, 87)]


def draw_plot_bokeh(logs,
                    metrics,
                    figsize=None,
                    max_epoch=None,
                    max_cols=2,
                    series_fmt={'training': '{}', 'validation': 'val_{}'},
                    metric2title={},
                    extra_plots=[],
                    fig_path=None):

    reset_output()
    output_notebook(hide_banner=True)
    clear_output(wait=True)

    figures = []

    if max_epoch:
        x_range = (1, max_epoch)
    else:
        x_range = None

    for metric_id, metric in enumerate(metrics):

        fig = figure(title=metric,
                     x_axis_label='epoch',
                     tools=['hover,pan,wheel_zoom,box_zoom,reset'],
                     plot_width=400,
                     plot_height=300,
                     x_range=x_range)

        for i, (serie_label, serie_fmt) in enumerate(series_fmt.items()):

            if serie_fmt.format(metric) in logs[0]:

                serie_metric_name = serie_fmt.format(metric)
                serie_metric_logs = [log[serie_metric_name] for log in logs]

                line = fig.line(range(1, len(logs) + 1), serie_metric_logs,
                                legend=serie_label, line_width=2, color=COLORS[i])
                fig.legend.location = "center_right"
                fig.legend.background_fill_alpha = 0.5
                fig.legend.padding = 5

        figures.append(fig)

    grid = gridplot(figures, ncols=max_cols)
    target = show(grid, notebook_handle=True)

    if fig_path:
        save(grid, filename=fig_path)

    push_notebook(handle=target)
