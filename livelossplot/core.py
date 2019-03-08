from __future__ import division
import warnings

import matplotlib
import matplotlib.pyplot as plt
from IPython.display import clear_output

MATPLOTLIB_TARGET = 'matplotlib'
NEPTUNE_TARGET = 'neptune'


def not_inline_warning():
    backend = matplotlib.get_backend()
    if "backend_inline" not in backend:
        warnings.warn("livelossplot requires inline plots.\nYour current backend is: {}\nRun in a Jupyter environment and execute '%matplotlib inline'.".format(backend))

# TODO
# * object-oriented API
# * only integer ticks


def draw_plot(logs, metrics, figsize=None, max_epoch=None,
              max_cols=2,
              series_fmt={'training': '{}', 'validation':'val_{}'},
              metric2title={},
              fig_path=None):
    clear_output(wait=True)
    plt.figure(figsize=figsize)

    extrema_logs = []
    for metric_id, metric in enumerate(metrics):
        plt.subplot((len(metrics) + 1) // max_cols + 1, max_cols, metric_id + 1)

        if max_epoch is not None:
            plt.xlim(1, max_epoch)

        for i, (serie_label, serie_fmt) in enumerate(series_fmt.items()):

            if serie_fmt.format(metric) in logs[0]:
                serie_metric_name = serie_fmt.format(metric)
                serie_metric_logs = [log[serie_metric_name] for log in logs]
                plt.plot(range(1, len(logs) + 1),
                         serie_metric_logs,
                         label=serie_label)

        plt.title(metric2title.get(metric, metric))
        plt.xlabel('epoch')
        plt.legend(loc='center right')

    plt.tight_layout()
    if fig_path is not None:
        plt.savefig(fig_path)
    plt.show()

def print_extrema(logs,
                  metrics,
                  extrema,
                  series_fmt={'training': '{}', 'validation':'val_{}'},
                  metric2title={}):

    extrema_logs = []
    for metric in metrics:

        values_fmt = ' (min: {min:8.3f}, max: {max:8.3f}, cur: {cur:8.3f})'

        serie_name_max_length = max([len(key) for key in series_fmt.keys()])

        # generic for any serie
        for i, (serie_label, serie_fmt) in enumerate(series_fmt.items()):
            serie_log_fmt = '\n{message: <{fill}}'.format(message=serie_label, fill=serie_name_max_length) + values_fmt

            if serie_fmt.format(metric) in logs[0]:
                serie_metric_name = serie_fmt.format(metric)
                serie_metric_logs = [log[serie_metric_name] for log in logs]

                log = serie_log_fmt.format(
                    min=extrema[serie_metric_name].get('min'),
                    max=extrema[serie_metric_name].get('max'),
                    cur=serie_metric_logs[-1])
                if i==0:
                    extrema_logs.append(metric2title.get(metric, metric) + ':' + log)
                else:
                    extrema_logs[-1] += log

    print('\n\n'.join(extrema_logs))
