from __future__ import division

import matplotlib.pyplot as plt
from keras.callbacks import Callback
from IPython.display import clear_output

# TODO
# * object-oriented API
# * only integer ticks

metric2printable = {
    "acc": "Accuracy",
    "mean_squared_error": "Mean squared error",
    "mean_absolute_error": "Mean absolute error",
    "mean_absolute_percentage_error": "Mean absolute percentage error",
    # etc
    "categorical_crossentropy": "Log-loss",
    "sparse_categorical_crossentropy": "Log-loss",
    "binary_crossentropy": "Log-loss",
    "kullback_leibler_divergence": "Log-loss"
}

class PlotLosses(Callback):
    def __init__(self, figsize=None, cell_size=(6, 4), dynamic_x_axis=False, max_cols=2):
        self.figsize = figsize
        self.cell_size = cell_size
        self.dynamic_x_axis = dynamic_x_axis
        self.max_cols = max_cols

    def on_train_begin(self, logs={}):

        self.base_metrics = [metric for metric in self.params['metrics'] if not metric.startswith('val_')]
        if self.figsize is None:
            self.figsize = (
                self.max_cols * self.cell_size[0],
                ((len(self.base_metrics) + 1) // self.max_cols + 1) * self.cell_size[1]
            )
        self.loss_metric = self.model.loss
        self.max_epoch = self.params['epochs']

        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)

        clear_output(wait=True)
        plt.figure(figsize=self.figsize)

        for metric_id, metric in enumerate(self.base_metrics):
            plt.subplot((len(self.base_metrics) + 1) // self.max_cols + 1, self.max_cols, metric_id + 1)

            if not self.dynamic_x_axis:
                plt.xlim(1, self.max_epoch)

            plt.plot(range(1, len(self.logs) + 1),
                     [log[metric] for log in self.logs],
                     label="training")

            if self.params['do_validation']:
                plt.plot(range(1, len(self.logs) + 1),
                         [log['val_' + metric] for log in self.logs],
                         label="validation")

            if metric == 'loss':
                plt.title(metric2printable.get(self.loss_metric, self.loss_metric) + " (cost function)")
            else:
                plt.title(metric2printable.get(metric, metric))

            plt.xlabel('epoch')
            plt.legend(loc='center right')

        plt.tight_layout()
        plt.show();
