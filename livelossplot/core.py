from __future__ import division
import warnings

import matplotlib
import matplotlib.pyplot as plt
from IPython.display import clear_output


def not_inline_warning():
    backend = matplotlib.get_backend()
    if "backend_inline" not in backend:
        warnings.warn("livelossplot requires inline plots.\nYour current backend is: {}\nRun in a Jupyter environment and execute '%matplotlib inline'.".format(backend))

# TODO
# * object-oriented API
# * only integer ticks


def draw_plot(logs, metrics, figsize=None, max_epoch=None,
              max_cols=2,
              validation_fmt="val_{}",
              metric2title={},
              extrema=None):
    clear_output(wait=True)
    plt.figure(figsize=figsize)

    for metric_id, metric in enumerate(metrics):
        plt.subplot((len(metrics) + 1) // max_cols + 1, max_cols, metric_id + 1)

        if max_epoch is not None:
            plt.xlim(1, max_epoch)

        plt.plot(range(1, len(logs) + 1),
                 [log[metric] for log in logs],
                 label="training")

        annotation_fmt = '{phase:20} minimum: {min:10.4}    maximum: {max:10.4}'
        annotation = None
        if extrema:
            annotation = annotation_fmt\
                .format(phase='training:',
                        min=extrema[metric].get('min', float('inf')),
                        max=extrema[metric].get('max', -float('inf')))

        if validation_fmt.format(metric) in logs[0]:
            val_metric = validation_fmt.format(metric)
            plt.plot(range(1, len(logs) + 1),
                     [log[val_metric] for log in logs],
                     label="validation")
            if extrema:
                annotation += '\n' + annotation_fmt\
                    .format(phase='validation:',
                            min=extrema[val_metric].get('min', float('inf')),
                            max=extrema[val_metric].get('max', -float('inf')))

        plt.title(metric2title.get(metric, metric))
        plt.xlabel('epoch')
        plt.legend(loc='center right')
        if annotation:
            plt.annotate(annotation, (0, 0), (0, -40),
                         xycoords='axes fraction', textcoords='offset points', va='top')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.show()
