from __future__ import division

import matplotlib
import matplotlib.pyplot as plt
from IPython.display import clear_output

def check_inline():
    return "backend_inline" in matplotlib.get_backend()

# TODO
# * check backend
# * object-oriented API
# * only integer ticks

def draw_plot(logs, metrics, figsize=None, max_epoch=None,
              max_cols=2,
              validation_fmt="val_{}",
              metric2title={}):
    clear_output(wait=True)
    plt.figure(figsize=figsize)

    for metric_id, metric in enumerate(metrics):
        plt.subplot((len(metrics) + 1) // max_cols + 1, max_cols, metric_id + 1)

        if max_epoch is not None:
            plt.xlim(1, max_epoch)

        plt.plot(range(1, len(logs) + 1),
                 [log[metric] for log in logs],
                 label="training")

        if validation_fmt.format(metric) in logs[0]:
            plt.plot(range(1, len(logs) + 1),
                     [log[validation_fmt.format(metric)] for log in logs],
                     label="validation")

        plt.title(metric2title.get(metric, metric))
        plt.xlabel('epoch')
        plt.legend(loc='center right')

    plt.tight_layout()
    plt.show();
